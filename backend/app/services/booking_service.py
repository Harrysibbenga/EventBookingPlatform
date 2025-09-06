# app/services/booking_service.py
"""
Enhanced booking service with duplicate detection and error handling.
"""

from datetime import date, datetime, timedelta
from typing import Dict, Any, Optional, Tuple, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from app.models.booking import Booking, BookingStatus, EventType
from app.schemas.booking import BookingCreate, BookingUpdate, BookingFilter
from app.schemas.responses import (
    create_duplicate_booking_response, create_minimum_timeframe_response
)
from app.utils.exceptions import ValidationError, BookingServiceError
from app.utils.logger import get_logger
from app.core.config import get_settings
from app.services.email_service import email_service

logger = get_logger(__name__)
settings = get_settings()


class BookingService:
    """Enhanced booking service with comprehensive validation and error handling."""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def create_booking(self, booking_data: BookingCreate) -> Booking:
        """Create a new booking with enhanced validation and duplicate detection."""
        
        # Enhanced validation with user-friendly error responses
        await self._validate_booking_creation(booking_data)
        
        try:
            # Create booking instance
            booking = Booking(
                event_type=booking_data.event_type,
                event_date=booking_data.event_date,
                event_time=booking_data.event_time,
                duration_hours=booking_data.duration_hours or 6,
                guest_count=booking_data.guest_count,
                venue_name=booking_data.venue_name,
                venue_address=booking_data.venue_address,
                venue_type=booking_data.venue_type,
                budget_min=booking_data.budget_min,
                budget_max=booking_data.budget_max,
                budget_flexible=booking_data.budget_flexible,
                services_needed=booking_data.services_needed,
                special_requirements=booking_data.special_requirements,
                contact_name=booking_data.contact_name.strip(),
                contact_email=booking_data.contact_email.lower().strip(),
                contact_phone=booking_data.contact_phone,
                preferred_contact=booking_data.preferred_contact,
                how_heard_about_us=booking_data.how_heard_about_us,
                previous_client=booking_data.previous_client,
                is_priority=self._determine_priority(booking_data),
                status=BookingStatus.PENDING
            )
            
            # Save to database
            self.db.add(booking)
            self.db.commit()
            self.db.refresh(booking)
            
            # Send confirmation emails asynchronously
            await self._send_booking_notifications(booking)
            
            logger.info(f"Created booking {booking.id} for {booking.contact_email}")
            return booking
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to create booking: {e}")
            raise BookingServiceError(f"Failed to create booking: {str(e)}")
    
    async def _validate_booking_creation(self, booking_data: BookingCreate):
        """Enhanced validation with user-friendly error messages."""

        event_date = booking_data.event_date
    
        existing_booking = self.db.query(Booking).filter(
            and_(
                Booking.contact_email == booking_data.contact_email.lower().strip(),
                func.date(Booking.event_date) == event_date,  # Compare just the date part
                Booking.status != BookingStatus.CANCELLED
            )
        ).first()
        
        if existing_booking:
            # Create detailed duplicate booking error
            duplicate_error = create_duplicate_booking_response(
                existing_booking=existing_booking,
                business_email=getattr(settings, 'BUSINESS_EMAIL', 'info@business.com'),
                business_phone=getattr(settings, 'BUSINESS_PHONE', None)
            )
            
            raise ValidationError(
                message=duplicate_error.message,
                error_code="DUPLICATE_BOOKING",
                details=duplicate_error.dict()
            )
        
        # 2. Check minimum timeframe (configurable, currently disabled)
        # Note: You requested no minimum timeframe for now, but here's the structure
        minimum_days = getattr(settings, 'MINIMUM_BOOKING_DAYS', 0)  # Set to 0 for no minimum
        
        if minimum_days > 0:
            days_until_event = (booking_data.event_date - date.today()).days
            
            if days_until_event < minimum_days:
                # Check if rush booking is available for large events
                if booking_data.guest_count > 50 and days_until_event < 7:
                    timeframe_error = create_minimum_timeframe_response(
                        days_until_event=days_until_event,
                        minimum_days=7,  # Minimum for large events
                        guest_count=booking_data.guest_count,
                        business_email=getattr(settings, 'BUSINESS_EMAIL', 'info@business.com'),
                        business_phone=getattr(settings, 'BUSINESS_PHONE', None)
                    )
                    
                    raise ValidationError(
                        message=timeframe_error.message,
                        error_code="MINIMUM_TIMEFRAME_ERROR",
                        details=timeframe_error.dict()
                    )
        
        # 3. Check event date is not too far in the future (2 years)
        max_future_date = date.today() + timedelta(days=730)
        if booking_data.event_date > max_future_date:
            raise ValidationError(
                message="We're currently accepting bookings up to 2 years in advance. Please contact us directly for events further in the future.",
                error_code="DATE_TOO_FAR",
                details={
                    "max_booking_date": max_future_date.isoformat(),
                    "contact_email": getattr(settings, 'BUSINESS_EMAIL', 'info@business.com'),
                    "contact_phone": getattr(settings, 'BUSINESS_PHONE', None)
                }
            )
        
        # 4. Validate guest count for event type (warnings, not errors)
        if booking_data.event_type == EventType.WEDDING and booking_data.guest_count < 10:
            logger.warning(f"Small guest count ({booking_data.guest_count}) for wedding booking")
        
        # 5. Business rule validations
        if booking_data.budget_min and booking_data.budget_max:
            if booking_data.budget_max < booking_data.budget_min:
                raise ValidationError(
                    message="Maximum budget must be greater than minimum budget",
                    error_code="INVALID_BUDGET_RANGE",
                    details={
                        "budget_min": str(booking_data.budget_min),
                        "budget_max": str(booking_data.budget_max)
                    }
                )
    
    def _determine_priority(self, booking_data: BookingCreate) -> bool:
        """Determine if booking should be marked as priority."""
        
        # Priority criteria
        priority_factors = []
        
        # 1. Event date within 30 days
        days_until_event = (booking_data.event_date - date.today()).days
        if days_until_event <= 30:
            priority_factors.append("short_notice")
        
        # 2. Large guest count (100+ guests)
        if booking_data.guest_count >= 100:
            priority_factors.append("large_event")
        
        # 3. High budget (£5000+)
        if booking_data.budget_min and booking_data.budget_min >= 5000:
            priority_factors.append("high_budget")
        
        # 4. Wedding events are typically higher priority
        if booking_data.event_type == EventType.WEDDING:
            priority_factors.append("wedding")
        
        # 5. Previous client
        if booking_data.previous_client:
            priority_factors.append("returning_client")
        
        # Mark as priority if 2 or more factors
        is_priority = len(priority_factors) >= 2
        
        if is_priority:
            logger.info(f"Marking booking as priority due to: {', '.join(priority_factors)}")
        
        return is_priority
    
    async def _send_booking_notifications(self, booking: Booking):
        """Send confirmation and admin notification emails."""
        try:
            # Prepare booking data for email templates
            booking_data = {
                "id": booking.id,
                "contact_name": booking.contact_name,
                "contact_email": booking.contact_email,
                "contact_phone": booking.contact_phone,
                "event_type": booking.event_type.value,
                "event_date": booking.event_date,
                "event_time": booking.event_time,
                "guest_count": booking.guest_count,
                "venue_name": booking.venue_name,
                "budget_min": booking.budget_min,
                "budget_max": booking.budget_max,
                "services_needed": booking.services_needed,
                "special_requirements": booking.special_requirements,
                "preferred_contact": booking.preferred_contact.value,
                "how_heard_about_us": booking.how_heard_about_us,
                "previous_client": booking.previous_client,
                "created_at": booking.created_at
            }
            
            # Send confirmation email to client
            await email_service.send_booking_confirmation(booking_data)
            
            # Send notification email to admin
            await email_service.send_admin_notification("booking", booking_data)
            
        except Exception as e:
            logger.error(f"Failed to send booking notifications: {e}")
            # Don't raise exception here - booking is already created
    
    def get_bookings(
        self,
        filters: Optional[BookingFilter] = None,
        page: int = 1,
        per_page: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> Tuple[List[Booking], int]:
        """Get paginated list of bookings with filtering."""
        
        query = self.db.query(Booking)
        
        # Apply filters
        if filters:
            query = self._apply_filters(query, filters)
        
        # Get total count before pagination
        total = query.count()
        
        # Apply sorting
        sort_column = getattr(Booking, sort_by, Booking.created_at)
        if sort_order.lower() == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        
        # Apply pagination
        offset = (page - 1) * per_page
        bookings = query.offset(offset).limit(per_page).all()
        
        return bookings, total
    
    def get_booking(self, booking_id: int) -> Optional[Booking]:
        """Get a specific booking by ID."""
        return self.db.query(Booking).filter(Booking.id == booking_id).first()
    
    def update_booking(self, booking_id: int, update_data: BookingUpdate) -> Optional[Booking]:
        """Update a booking inquiry."""
        booking = self.get_booking(booking_id)
        if not booking:
            return None
        
        # Update fields
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(booking, field, value)
        
        booking.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(booking)
        
        return booking
    
    def delete_booking(self, booking_id: int) -> bool:
        """Archive a booking (soft delete)."""
        booking = self.get_booking(booking_id)
        if not booking:
            return False
        
        booking.is_archived = True
        booking.updated_at = datetime.utcnow()
        
        self.db.commit()
        return True
    
    def get_booking_stats(self) -> Dict[str, Any]:
        """Get booking statistics for dashboard."""
        
        # Basic counts
        total_bookings = self.db.query(Booking).count()
        pending_bookings = self.db.query(Booking).filter(
            Booking.status == BookingStatus.PENDING
        ).count()
        priority_bookings = self.db.query(Booking).filter(
            Booking.is_priority == True
        ).count()
        
        # This month bookings
        start_of_month = date.today().replace(day=1)
        this_month_bookings = self.db.query(Booking).filter(
            Booking.created_at >= start_of_month
        ).count()
        
        # Average guest count
        avg_guest_result = self.db.query(
            func.avg(Booking.guest_count)
        ).scalar()
        avg_guest_count = float(avg_guest_result) if avg_guest_result else 0.0
        
        # Popular event types
        event_type_counts = self.db.query(
            Booking.event_type,
            func.count(Booking.id).label('count')
        ).group_by(Booking.event_type).all()
        
        popular_event_types = [
            {
                "event_type": event_type.value,
                "count": count,
                "label": event_type.value.replace("_", " ").title()
            }
            for event_type, count in event_type_counts
        ]
        
        # Monthly trends (last 6 months)
        monthly_trends = []
        for i in range(6):
            month_start = (date.today().replace(day=1) - timedelta(days=32*i)).replace(day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            month_count = self.db.query(Booking).filter(
                and_(
                    Booking.created_at >= month_start,
                    Booking.created_at <= month_end
                )
            ).count()
            
            monthly_trends.append({
                "month": month_start.strftime("%Y-%m"),
                "count": month_count
            })
        
        return {
            "total_bookings": total_bookings,
            "pending_bookings": pending_bookings,
            "this_month_bookings": this_month_bookings,
            "priority_bookings": priority_bookings,
            "avg_guest_count": avg_guest_count,
            "popular_event_types": popular_event_types,
            "monthly_trends": list(reversed(monthly_trends))
        }
    
    def get_upcoming_events(self, days_ahead: int = 30) -> List[Booking]:
        """Get bookings with events in the next N days."""
        cutoff_date = date.today() + timedelta(days=days_ahead)
        
        return self.db.query(Booking).filter(
            and_(
                Booking.event_date <= cutoff_date,
                Booking.event_date >= date.today(),
                Booking.status.in_([BookingStatus.CONFIRMED, BookingStatus.QUOTED])
            )
        ).order_by(Booking.event_date).all()
    
    def get_overdue_bookings(self) -> List[Booking]:
        """Get bookings that need follow-up."""
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        
        return self.db.query(Booking).filter(
            and_(
                Booking.status == BookingStatus.PENDING,
                Booking.created_at <= cutoff_time,
                Booking.contacted_at.is_(None)
            )
        ).all()
    
    def search_bookings(self, search_term: str) -> List[Booking]:
        """Search bookings by name, email, or notes."""
        search_pattern = f"%{search_term.lower()}%"
        
        return self.db.query(Booking).filter(
            or_(
                func.lower(Booking.contact_name).like(search_pattern),
                func.lower(Booking.contact_email).like(search_pattern),
                func.lower(Booking.admin_notes).like(search_pattern),
                func.lower(Booking.special_requirements).like(search_pattern)
            )
        ).all()
    
    def _apply_filters(self, query, filters: BookingFilter):
        """Apply filters to booking query."""
        if filters.status:
            query = query.filter(Booking.status == filters.status)
        
        if filters.event_type:
            query = query.filter(Booking.event_type == filters.event_type)
        
        if filters.is_priority is not None:
            query = query.filter(Booking.is_priority == filters.is_priority)
        
        if filters.is_archived is not None:
            query = query.filter(Booking.is_archived == filters.is_archived)
        
        if filters.date_from:
            query = query.filter(Booking.event_date >= filters.date_from)
        
        if filters.date_to:
            query = query.filter(Booking.event_date <= filters.date_to)
        
        if filters.guest_count_min:
            query = query.filter(Booking.guest_count >= filters.guest_count_min)
        
        if filters.guest_count_max:
            query = query.filter(Booking.guest_count <= filters.guest_count_max)
        
        if filters.budget_min:
            query = query.filter(
                or_(
                    Booking.budget_min >= filters.budget_min,
                    Booking.budget_max >= filters.budget_min
                )
            )
        
        if filters.budget_max:
            query = query.filter(
                or_(
                    Booking.budget_min <= filters.budget_max,
                    Booking.budget_max <= filters.budget_max
                )
            )
        
        if filters.search:
            search_pattern = f"%{filters.search.lower()}%"
            query = query.filter(
                or_(
                    func.lower(Booking.contact_name).like(search_pattern),
                    func.lower(Booking.contact_email).like(search_pattern),
                    func.lower(Booking.admin_notes).like(search_pattern),
                    func.lower(Booking.special_requirements).like(search_pattern)
                )
            )
        
        return query