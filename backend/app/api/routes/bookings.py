"""
API routes for booking management.
Handles HTTP requests for booking inquiries and administration.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
import math

from app.core.database import get_db
from app.schemas.booking import (
    BookingCreate, BookingResponse, BookingUpdate, BookingList,
    BookingStats, BookingFilter, BookingConfirmation, BookingFormOptions,
    EventTypeOption, ServiceOption
)
from app.services.booking_service import BookingService
from app.models.booking import EventType, ContactMethod, BookingStatus
from app.utils.logger import get_logger
from app.utils.exceptions import BookingServiceError, ValidationError

logger = get_logger(__name__)
router = APIRouter(prefix="/bookings")


@router.post("/", response_model=BookingConfirmation, status_code=201)
async def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new booking inquiry.
    
    This endpoint handles the submission of event booking inquiries from the frontend.
    It validates the data, creates the booking record, and sends confirmation emails.
    """
    try:
        service = BookingService(db)
        booking = await service.create_booking(booking_data)
        
        # Generate confirmation response
        confirmation_number = f"BK{booking.id:06d}"
        
        return BookingConfirmation(
            success=True,
            booking_id=booking.id,
            message="Your booking inquiry has been successfully submitted!",
            confirmation_number=confirmation_number,
            next_steps=[
                "We will review your inquiry within 24 hours",
                "A team member will contact you to discuss details",
                "You'll receive a detailed quote and contract",
                "Once approved, we'll secure your event date"
            ]
        )
        
    except ValidationError as e:
        logger.warning(f"Booking validation error: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    
    except BookingServiceError as e:
        logger.error(f"Booking service error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process booking inquiry")
    
    except Exception as e:
        logger.error(f"Unexpected error creating booking: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=BookingList)
def get_bookings(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[BookingStatus] = Query(None, description="Filter by status"),
    event_type: Optional[EventType] = Query(None, description="Filter by event type"),
    is_priority: Optional[bool] = Query(None, description="Filter by priority"),
    is_archived: Optional[bool] = Query(False, description="Include archived bookings"),
    search: Optional[str] = Query(None, min_length=3, description="Search term"),
    sort_by: str = Query("created_at", description="Sort field"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """
    Get paginated list of booking inquiries.
    
    Admin endpoint for viewing and managing booking inquiries with filtering,
    searching, and sorting capabilities.
    """
    try:
        # Create filter object
        filters = BookingFilter(
            status=status,
            event_type=event_type,
            is_priority=is_priority,
            is_archived=is_archived,
            search=search
        )
        
        service = BookingService(db)
        bookings, total = service.get_bookings(
            filters=filters,
            page=page,
            per_page=per_page,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        # Calculate pagination info
        pages = math.ceil(total / per_page)
        has_next = page < pages
        has_prev = page > 1
        
        return BookingList(
            bookings=[BookingResponse.from_orm(booking) for booking in bookings],
            total=total,
            page=page,
            per_page=per_page,
            pages=pages,
            has_next=has_next,
            has_prev=has_prev
        )
        
    except Exception as e:
        logger.error(f"Error fetching bookings: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch bookings")


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(
    booking_id: int = Path(..., ge=1, description="Booking ID"),
    db: Session = Depends(get_db)
):
    """
    Get a specific booking inquiry by ID.
    
    Admin endpoint for viewing detailed booking information.
    """
    try:
        service = BookingService(db)
        booking = service.get_booking(booking_id)
        
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        return BookingResponse.from_orm(booking)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching booking {booking_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch booking")


@router.put("/{booking_id}", response_model=BookingResponse)
def update_booking(
    booking_id: int = Path(..., ge=1, description="Booking ID"),
    update_data: BookingUpdate = ...,
    db: Session = Depends(get_db)
):
    """
    Update a booking inquiry.
    
    Admin endpoint for updating booking status, notes, and other administrative fields.
    """
    try:
        service = BookingService(db)
        booking = service.update_booking(booking_id, update_data)
        
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        return BookingResponse.from_orm(booking)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating booking {booking_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update booking")


@router.delete("/{booking_id}")
def delete_booking(
    booking_id: int = Path(..., ge=1, description="Booking ID"),
    db: Session = Depends(get_db)
):
    """
    Archive a booking inquiry.
    
    Admin endpoint for soft-deleting (archiving) booking inquiries.
    """
    try:
        service = BookingService(db)
        success = service.delete_booking(booking_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        return {"message": "Booking archived successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error archiving booking {booking_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to archive booking")


@router.get("/stats/dashboard", response_model=BookingStats)
def get_booking_stats(db: Session = Depends(get_db)):
    """
    Get booking statistics for admin dashboard.
    
    Returns aggregated statistics including counts, trends, and analytics.
    """
    try:
        service = BookingService(db)
        stats = service.get_booking_stats()
        
        return BookingStats(**stats)
        
    except Exception as e:
        logger.error(f"Error fetching booking stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch statistics")


@router.get("/upcoming/events")
def get_upcoming_events(
    days_ahead: int = Query(30, ge=1, le=365, description="Days to look ahead"),
    db: Session = Depends(get_db)
):
    """
    Get upcoming confirmed events.
    
    Admin endpoint for viewing events scheduled in the near future.
    """
    try:
        service = BookingService(db)
        bookings = service.get_upcoming_events(days_ahead)
        
        return [BookingResponse.from_orm(booking) for booking in bookings]
        
    except Exception as e:
        logger.error(f"Error fetching upcoming events: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch upcoming events")


@router.get("/overdue/follow-ups")
def get_overdue_bookings(db: Session = Depends(get_db)):
    """
    Get bookings that need follow-up.
    
    Admin endpoint for identifying bookings that haven't been contacted
    within the expected timeframe.
    """
    try:
        service = BookingService(db)
        bookings = service.get_overdue_bookings()
        
        return [BookingResponse.from_orm(booking) for booking in bookings]
        
    except Exception as e:
        logger.error(f"Error fetching overdue bookings: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch overdue bookings")


@router.get("/search/inquiries")
def search_bookings(
    q: str = Query(..., min_length=3, description="Search query"),
    db: Session = Depends(get_db)
):
    """
    Search booking inquiries.
    
    Admin endpoint for searching bookings by name, email, or notes.
    """
    try:
        service = BookingService(db)
        bookings = service.search_bookings(q)
        
        return [BookingResponse.from_orm(booking) for booking in bookings]
        
    except Exception as e:
        logger.error(f"Error searching bookings: {e}")
        raise HTTPException(status_code=500, detail="Failed to search bookings")


@router.get("/form/options", response_model=BookingFormOptions)
def get_form_options():
    """
    Get configuration options for the booking form.
    
    Public endpoint that provides form options like event types,
    services, and other configuration data for the frontend.
    """
    try:
        # Event type options
        event_types = [
            EventTypeOption(
                value=EventType.WEDDING.value,
                label="Wedding",
                description="Ceremonies, receptions, and wedding celebrations"
            ),
            EventTypeOption(
                value=EventType.BIRTHDAY.value,
                label="Birthday Party",
                description="Birthday celebrations and milestone parties"
            ),
            EventTypeOption(
                value=EventType.CORPORATE.value,
                label="Corporate Event",
                description="Business meetings, conferences, and company events"
            ),
            EventTypeOption(
                value=EventType.ANNIVERSARY.value,
                label="Anniversary",
                description="Wedding anniversaries and milestone celebrations"
            ),
            EventTypeOption(
                value=EventType.GRADUATION.value,
                label="Graduation",
                description="Graduation parties and academic celebrations"
            ),
            EventTypeOption(
                value=EventType.BABY_SHOWER.value,
                label="Baby Shower",
                description="Baby showers and gender reveal parties"
            ),
            EventTypeOption(
                value=EventType.ENGAGEMENT.value,
                label="Engagement Party",
                description="Engagement celebrations and proposal parties"
            ),
            EventTypeOption(
                value=EventType.RETIREMENT.value,
                label="Retirement Party",
                description="Retirement celebrations and farewell events"
            ),
            EventTypeOption(
                value=EventType.HOLIDAY.value,
                label="Holiday Event",
                description="Holiday parties and seasonal celebrations"
            ),
            EventTypeOption(
                value=EventType.OTHER.value,
                label="Other",
                description="Custom events and special occasions"
            )
        ]
        
        # Service options
        services = [
            ServiceOption(
                id="catering",
                name="Catering",
                description="Full-service catering and menu planning",
                base_price=25.00,
                is_popular=True
            ),
            ServiceOption(
                id="photography",
                name="Photography",
                description="Professional event photography",
                base_price=500.00,
                is_popular=True
            ),
            ServiceOption(
                id="videography",
                name="Videography",
                description="Event videography and editing",
                base_price=800.00
            ),
            ServiceOption(
                id="dj",
                name="DJ Services",
                description="Professional DJ and sound system",
                base_price=400.00,
                is_popular=True
            ),
            ServiceOption(
                id="live_band",
                name="Live Band",
                description="Live music entertainment",
                base_price=1200.00
            ),
            ServiceOption(
                id="decoration",
                name="Decoration",
                description="Event decoration and styling",
                base_price=300.00,
                is_popular=True
            ),
            ServiceOption(
                id="flowers",
                name="Floral Arrangements",
                description="Fresh flower arrangements and centerpieces",
                base_price=200.00
            ),
            ServiceOption(
                id="lighting",
                name="Lighting",
                description="Professional event lighting design",
                base_price=350.00
            ),
            ServiceOption(
                id="planning",
                name="Event Planning",
                description="Full event planning and coordination",
                base_price=1000.00,
                is_popular=True
            ),
            ServiceOption(
                id="bartending",
                name="Bartending",
                description="Professional bartending services",
                base_price=300.00
            )
        ]
        
        # Contact method options
        contact_methods = [
            {"value": ContactMethod.EMAIL.value, "label": "Email"},
            {"value": ContactMethod.PHONE.value, "label": "Phone"},
            {"value": ContactMethod.EITHER.value, "label": "Either Email or Phone"}
        ]
        
        # Venue types
        venue_types = [
            "Indoor",
            "Outdoor",
            "Garden",
            "Beach",
            "Church",
            "Reception Hall",
            "Restaurant",
            "Hotel",
            "Private Residence",
            "Community Center",
            "Country Club",
            "Barn",
            "Rooftop",
            "Other"
        ]
        
        # Time slots
        time_slots = [
            "9:00 AM", "9:30 AM", "10:00 AM", "10:30 AM", "11:00 AM", "11:30 AM",
            "12:00 PM", "12:30 PM", "1:00 PM", "1:30 PM", "2:00 PM", "2:30 PM",
            "3:00 PM", "3:30 PM", "4:00 PM", "4:30 PM", "5:00 PM", "5:30 PM",
            "6:00 PM", "6:30 PM", "7:00 PM", "7:30 PM", "8:00 PM", "8:30 PM",
            "9:00 PM", "9:30 PM", "10:00 PM"
        ]
        
        return BookingFormOptions(
            event_types=event_types,
            services=services,
            contact_methods=contact_methods,
            venue_types=venue_types,
            time_slots=time_slots,
            max_guest_count=1000,
            min_advance_days=7
        )
        
    except Exception as e:
        logger.error(f"Error fetching form options: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch form options")