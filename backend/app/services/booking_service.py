"""
Booking service for handling business logic related to event bookings.
Provides high-level operations for booking management and processing.
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc, func, extract
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, date, timedelta
import json

from app.models.booking import Booking, EventType, BookingStatus, ContactMethod
from app.schemas.booking import BookingCreate, BookingUpdate, BookingFilter
from app.services.email_service import email_service
from app.utils.logger import get_logger
from app.utils.exceptions import BookingServiceError, ValidationError

logger = get_logger(__name__)


class BookingService:
    """Service class for booking-related business logic."""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def create_booking(self, booking_data: BookingCreate) -> Booking:
        """
        Create a new booking inquiry.
        
        Args:
            booking_data: Booking creation data
            
        Returns:
            Booking: Created booking instance
        """
        try:
            # Validate business rules
            await self._validate_booking_creation(booking_data)
            
            # Create booking instance
            booking = Booking(
                # Event details
                event_type=booking_data.event_type,
                event_date=booking_data.event_date,
                event_time=booking_data.event_time,
                duration_hours=booking_data.duration_hours,
                guest_count=booking_data.guest_count,
                
                # Venue information
                venue_name=booking_data.venue_name,
                venue_address=booking_data.venue_address,
                venue_type=booking_data.venue_type,
                
                # Budget information
                budget_min=booking_data.budget_min,
                budget_max=booking_data.budget_max,
                budget_flexible=booking_data.budget_flexible,
                
                # Services and requirements
                services_needed=booking_data.services_needed,
                special_requirements=booking_data.special_requirements,
                
                # Contact information
                contact_name=booking_data.contact_name,
                contact_email=booking_data.contact_email.lower(),
                contact_phone=booking_data.contact_phone,
                preferred_contact=booking_data.preferred_contact,
                
                # Additional information
                how_heard_about_us=booking_data.how_heard_about_us,
                previous_client=booking_data.previous_client,
                
                # Set initial status and flags
                status=BookingStatus.PENDING,
                is_priority=self._determine_priority(booking_data),
                requires_consultation=True
            )
            
            # Save to database
            self.db.add(booking)
            self.db.commit()
            self.db.refresh(booking)
            
            # Send notifications
            await self._send_booking_notifications(booking)
            
            logger.info(f"Created booking inquiry {booking.id} for {booking.contact_name}")
            return booking
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to create booking: {e}")
            raise BookingServiceError(f"Failed to create booking: {e}")
    
    def get_booking(self, booking_id: int) -> Optional[Booking]:
        """Get booking by ID."""
        return self.db.query(Booking).filter(Booking.id == booking_id).first()
    
    def get_bookings(
        self,
        filters: Optional[BookingFilter] = None,
        page: int = 1,
        per_page: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> Tuple[List[Booking], int]:
        """
        Get paginated list of bookings with optional filtering.
        
        Returns:
            Tuple: (bookings_list, total_count)
        """
        query = self.db.query(Booking)
        
        # Apply filters
        if filters:
            query = self._apply_filters(query, filters)
        
        # Get total count before pagination
        total = query.count()
        
        # Apply sorting
        if hasattr(Booking, sort_by):
            if sort_order.lower() == "desc":
                query = query.order_by(desc(getattr(Booking, sort_by)))
            else:
                query = query.order_by(asc(getattr(Booking, sort_by)))
        
        # Apply pagination
        offset = (page - 1) * per_page
        bookings = query.offset(offset).limit(per_page).all()
        
        return bookings, total
    
    def update_booking(self, booking_id: int, update_data: BookingUpdate) -> Optional[Booking]:
        """Update booking with admin data."""
        booking = self.get_booking(booking_id)
        if not booking:
            return None
        
        # Update fields
        for field, value in update_data.dict(exclude_unset=True).items():
            if hasattr(booking, field):
                setattr(booking, field, value)
        
        # Update timestamp
        booking.updated_at = datetime.utcnow()
        
        # Set specific timestamps based on status changes
        if update_data.status:
            if update_data.status == BookingStatus.CONTACTED and not booking.contacted_at:
                booking.contacted_at = datetime.utcnow()
            elif update_data.status == BookingStatus.QUOTED and not booking.quoted_at:
                booking.quoted_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(booking)
        
        logger.info(f"Updated booking {booking_id}")
        return booking
    
    def delete_booking(self, booking_id: int) -> bool:
        """Soft delete booking (archive it)."""
        booking = self.get_booking(booking_id)
        if not booking:
            return False
        
        booking.is_archived = True
        booking.updated_at = datetime.utcnow()
        self.db.commit()
        
        logger.info(f"Archived booking {booking_id}")
        return True
    
    def get_booking_stats(self) -> Dict[str, Any]:
        """Get booking statistics for dashboard."""
        try:
            # Basic counts
            total_bookings = self.db.query(Booking).count()
            pending_bookings = self.db.query(Booking).filter(
                Booking.status == BookingStatus.PENDING
            ).count()
            
            # This month bookings
            current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            this_month_bookings = self.db.query(Booking).filter(
                Booking.created_at >= current_month_start
            ).count()
            
            # Priority bookings
            priority_bookings = self.db.query(Booking).filter(
                Booking.is_priority == True
            ).count()
            
            # Average guest count
            avg_guest_count = self.db.query(func.avg(Booking.guest_count)).scalar() or 0
            
            # Popular event types
            event_type_stats = self.db.query(
                Booking.event_type,
                func.count(Booking.id).label('count')
            ).group_by(Booking.event_type).all()
            
            popular_event_types = [
                {"type": et.value, "count": count}
                for et, count in event_type_stats
            ]
            
            # Monthly trends (last 12 months)
            monthly_trends = []
            for i in range(12):
                month_start = (datetime.now() - timedelta(days=30*i)).replace(day=1)
                month_end = (month_start + timedelta(days=32)).replace(day=1)
                
                count = self.db.query(Booking).filter(
                    and_(
                        Booking.created_at >= month_start,
                        Booking.created_at < month_end
                    )
                ).count()
                
                monthly_trends.append({
                    "month": month_start.strftime("%Y-%m"),
                    "count": count
                })
            
            return {
                "total_bookings": total_bookings,
                "pending_bookings": pending_bookings,
                "this_month_bookings": this_month_bookings,
                "priority_bookings": priority_bookings,
                "avg_guest_count": round(avg_guest_count, 1),
                "popular_event_types": popular_event_types,
                "monthly_trends": list(reversed(monthly_trends))
            }
            
        except Exception as e:
            logger.error(f"Failed to get booking stats: {e}")
            return {}
    
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
        # Bookings older than 24 hours without contact
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        
        return self.db.query(Booking).filter(
            and_(
                Booking.status == BookingStatus.PENDING,
                Booking.created_at <= cutoff_time,
                Booking.contacted_at.is_(None)
            )
        ).all()
    
    async def _validate_booking_creation(self, booking_data: BookingCreate):
        """Validate booking creation business rules."""
        # Check for duplicate bookings (same email, same date)
        existing_booking = self.db.query(Booking).filter(
            and_(
                Booking.contact_email == booking_data.contact_email.lower(),
                Booking.event_date == booking_data.event_date,
                Booking.status != BookingStatus.CANCELLED
            )
        ).first()
        
        if existing_booking:
            raise ValidationError("A booking inquiry for this email and date already exists")
        
        # Check event date is not too far in the future (2 years)
        max_future_date = date.today() + timedelta(days=730)
        if booking_data.event_date > max_future_date:
            raise ValidationError("Event date cannot be more than 2 years in the future")
        
        # Validate guest count for event type
        if booking_data.event_type == EventType.WEDDING and booking_data.guest_count < 10:
            logger.warning(f"Small guest count ({booking_data.guest_count}) for wedding booking")
    
    def _determine_priority(self, booking_data: BookingCreate) -> bool:
        """Determine if booking should be marked as priority."""
        # Priority criteria
        priority_conditions = [
            # Large events (>200 guests)
            booking_data.guest_count > 200,
            
            # High budget events
            (booking_data.budget_min and booking_data.budget_min > 10000),
            
            # Events within 60 days - FIXED: Use consistent date types
            (booking_data.event_date - date.today()).days <= 60,
            
            # Corporate events (often have quick decision timelines)
            booking_data.event_type == EventType.CORPORATE,
            
            # Previous clients
            booking_data.previous_client
        ]
        
        return any(priority_conditions)
    
    async def _send_booking_notifications(self, booking: Booking):
        """Send confirmation and admin notification emails."""
        try:
            # Prepare booking data for email templates
            booking_data = {
                "id": booking.id,
                "contact_name": booking.contact_name,
                "contact_email": booking.contact_email,
                "contact_phone": booking.contact_phone,
                "preferred_contact": booking.preferred_contact.value if booking.preferred_contact else "email",
                "event_type": booking.event_type.value if booking.event_type else "unknown",
                "event_date": booking.event_date,
                "event_time": booking.event_time,
                "duration_hours": booking.duration_hours,
                "guest_count": booking.guest_count,
                "venue_name": booking.venue_name,
                "venue_address": booking.venue_address,
                "budget_min": booking.budget_min,
                "budget_max": booking.budget_max,
                "services_needed": booking.services_needed,
                "special_requirements": booking.special_requirements,
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
    
# Enhanced booking service validation with user-friendly error messages

from datetime import date, datetime, timedelta
from typing import Dict, Any, Optional
from app.utils.exceptions import ValidationError, BookingServiceError
from app.models.booking import BookingStatus

async def _validate_booking_creation(self, booking_data: BookingCreate):
    """Enhanced validation with user-friendly error messages."""
    
    # Check for duplicate bookings (same email, same date)
    existing_booking = self.db.query(Booking).filter(
        and_(
            Booking.contact_email == booking_data.contact_email.lower(),
            Booking.event_date == booking_data.event_date,
            Booking.status != BookingStatus.CANCELLED
        )
    ).first()
    
    if existing_booking:
        # Create detailed error message based on existing booking status
        error_details = self._create_duplicate_booking_error(existing_booking, booking_data)
        raise ValidationError(
            message=error_details["user_message"],
            error_code="DUPLICATE_BOOKING",
            details=error_details
        )
    
    # Check event date is not too far in the future (2 years)
    max_future_date = date.today() + timedelta(days=730)
    if booking_data.event_date > max_future_date:
        raise ValidationError(
            message="We're currently accepting bookings up to 2 years in advance. Please contact us directly for events further in the future.",
            error_code="DATE_TOO_FAR",
            details={
                "max_booking_date": max_future_date.isoformat(),
                "contact_email": settings.BUSINESS_EMAIL,
                "contact_phone": getattr(settings, 'BUSINESS_PHONE', None)
            }
        )
    
    # Check if event date is too soon (less than 7 days for large events)
    days_until_event = (booking_data.event_date - date.today()).days
    if days_until_event < 7 and booking_data.guest_count > 50:
        raise ValidationError(
            message="For events with more than 50 guests, we typically need at least 7 days notice. Please call us directly to discuss rush bookings.",
            error_code="SHORT_NOTICE_LARGE_EVENT",
            details={
                "days_until_event": days_until_event,
                "guest_count": booking_data.guest_count,
                "contact_phone": getattr(settings, 'BUSINESS_PHONE', None),
                "rush_booking_available": True
            }
        )
    
    # Validate guest count for event type
    if booking_data.event_type == EventType.WEDDING and booking_data.guest_count < 10:
        logger.warning(f"Small guest count ({booking_data.guest_count}) for wedding booking")
        # This is just a warning, not an error

def _create_duplicate_booking_error(self, existing_booking: Booking, new_booking_data: BookingCreate) -> Dict[str, Any]:
    """Create detailed error information for duplicate bookings."""
    
    # Generate reference number for existing booking
    reference_number = f"BK{existing_booking.id:06d}"
    
    # Determine user-friendly status
    status_messages = {
        BookingStatus.PENDING: "under review",
        BookingStatus.CONTACTED: "being processed",
        BookingStatus.QUOTED: "quoted and awaiting your response",
        BookingStatus.CONFIRMED: "confirmed",
        BookingStatus.COMPLETED: "completed"
    }
    
    status_text = status_messages.get(existing_booking.status, "being processed")
    
    # Calculate time since booking
    time_diff = datetime.utcnow() - existing_booking.created_at
    if time_diff.days > 0:
        time_text = f"{time_diff.days} day{'s' if time_diff.days != 1 else ''} ago"
    else:
        hours = int(time_diff.total_seconds() / 3600)
        if hours > 0:
            time_text = f"{hours} hour{'s' if hours != 1 else ''} ago"
        else:
            minutes = int(time_diff.total_seconds() / 60)
            time_text = f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    
    # Create appropriate user message based on status
    if existing_booking.status == BookingStatus.PENDING:
        user_message = f"""
        We already have a booking inquiry from you for {existing_booking.event_date.strftime('%B %d, %Y')}.
        
        Your inquiry (Reference: {reference_number}) was submitted {time_text} and is currently under review.
        
        What to do next:
        • Check your email for our confirmation message
        • We typically respond within 24 hours
        • If you need to make changes, please reply to our confirmation email
        • For urgent matters, contact us at {getattr(settings, 'BUSINESS_EMAIL', 'our business email')}
        
        Need to modify your request? Contact us directly instead of submitting again.
        """.strip()
    
    elif existing_booking.status == BookingStatus.CONTACTED:
        user_message = f"""
        Great news! We're already working on your booking inquiry for {existing_booking.event_date.strftime('%B %d, %Y')}.
        
        Your inquiry (Reference: {reference_number}) is currently being processed by our team.
        
        What to expect:
        • We should have a detailed quote for you soon
        • Check your email for updates from our team
        • If you haven't heard from us in 48 hours, please give us a call
        
        Need to add or change something? Reply to our last email or call us directly.
        """.strip()
    
    elif existing_booking.status == BookingStatus.QUOTED:
        user_message = f"""
        We've already sent you a quote for your event on {existing_booking.event_date.strftime('%B %d, %Y')}!
        
        Your inquiry (Reference: {reference_number}) has been quoted and is awaiting your response.
        
        Next steps:
        • Check your email for our detailed quote
        • Review the proposal and let us know if you'd like to proceed
        • If you need modifications, reply to our quote email
        • Ready to book? Follow the confirmation instructions in your quote
        
        Can't find our quote email? Contact us and we'll resend it immediately.
        """.strip()
    
    elif existing_booking.status == BookingStatus.CONFIRMED:
        user_message = f"""
        Wonderful! Your event on {existing_booking.event_date.strftime('%B %d, %Y')} is already confirmed.
        
        Your booking (Reference: {reference_number}) is all set!
        
        What's next:
        • You should have received a confirmation email with all details
        • We'll be in touch closer to your event date with final details
        • Need to make changes? Contact us directly
        
        Looking forward to making your event amazing!
        """.strip()
    
    else:  # Default message
        user_message = f"""
        We already have a booking inquiry from you for {existing_booking.event_date.strftime('%B %d, %Y')}.
        
        Your inquiry (Reference: {reference_number}) is currently {status_text}.
        
        Please check your email for updates, or contact us directly if you need assistance.
        """.strip()
    
    return {
        "user_message": user_message,
        "existing_booking_id": existing_booking.id,
        "reference_number": reference_number,
        "existing_status": existing_booking.status.value,
        "existing_created_at": existing_booking.created_at.isoformat(),
        "time_since_booking": time_text,
        "contact_info": {
            "email": getattr(settings, 'BUSINESS_EMAIL', None),
            "phone": getattr(settings, 'BUSINESS_PHONE', None)
        },
        "recommendations": self._get_user_recommendations(existing_booking)
    }

def _get_user_recommendations(self, existing_booking: Booking) -> List[str]:
    """Get specific recommendations based on booking status."""
    
    recommendations = []
    
    if existing_booking.status == BookingStatus.PENDING:
        recommendations = [
            "Check your email (including spam folder) for our confirmation",
            "If urgent, call us directly rather than submitting again",
            "We respond to all inquiries within 24 hours during business days"
        ]
    elif existing_booking.status == BookingStatus.CONTACTED:
        recommendations = [
            "Look for our follow-up email with next steps",
            "If you have additional requirements, reply to our email",
            "We'll send you a detailed quote within 2-3 business days"
        ]
    elif existing_booking.status == BookingStatus.QUOTED:
        recommendations = [
            "Review the quote we sent to your email",
            "Contact us if you need any modifications",
            "Confirm your booking by following the quote instructions",
            "Quote is valid for 30 days from the send date"
        ]
    elif existing_booking.status == BookingStatus.CONFIRMED:
        recommendations = [
            "Your event is confirmed - no further action needed",
            "We'll contact you 2 weeks before your event with final details",
            "Any changes should be communicated directly to us",
            "Thank you for choosing us for your special event!"
        ]
    
    return recommendations


# Frontend error handling helper (for your Vue component)
"""
// Enhanced frontend error handling
const handleBookingError = (error: any) => {
  if (error.response?.data?.error_code === 'DUPLICATE_BOOKING') {
    // Show detailed duplicate booking information
    const details = error.response.data
    
    showModal({
      title: "Booking Already Exists",
      message: details.message,
      type: "info",
      actions: [
        {
          text: "Check Email",
          action: () => window.open('mailto:', '_blank')
        },
        {
          text: "Contact Us", 
          action: () => window.open(`tel:${details.contact_info.phone}`, '_blank')
        }
      ]
    })
    
  } else if (error.response?.data?.error_code === 'SHORT_NOTICE_LARGE_EVENT') {
    // Handle rush booking scenario
    const details = error.response.data
    
    showModal({
      title: "Rush Booking Available",
      message: details.message,
      type: "warning",
      actions: [
        {
          text: "Call Now",
          primary: true,
          action: () => window.open(`tel:${details.contact_phone}`, '_blank')
        },
        {
          text: "Modify Date",
          action: () => {
            // Allow user to change date
            currentStep.value = 0
          }
        }
      ]
    })
    
  } else {
    // Generic error handling
    showModal({
      title: "Booking Submission Error",
      message: error.response?.data?.message || "Please try again or contact us directly.",
      type: "error",
      actions: [
        {
          text: "Try Again",
          action: () => handleSubmit()
        },
        {
          text: "Contact Us",
          action: () => window.open(`mailto:${businessEmail}`, '_blank')
        }
      ]
    })
  }
}
"""