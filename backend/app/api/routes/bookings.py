# app/api/routes/bookings.py
"""
Enhanced API routes for booking management with comprehensive error handling.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import Optional, Union
from datetime import datetime
import math
import uuid

from app.core.config import get_settings
from app.core.database import get_db
from app.schemas.booking import (
    BookingCreate, BookingResponse, BookingUpdate, BookingList,
    BookingStats, BookingFilter, BookingConfirmation, BookingFormOptions,
    EventTypeOption, ServiceOption
)
from app.schemas.responses import ( DuplicateBookingError, MinimumTimeframeError,
    ValidationErrorResponse, ServiceErrorResponse, ContactInfo
)
from app.services.booking_service import BookingService
from app.models.booking import EventType, ContactMethod, BookingStatus
from app.utils.logger import get_logger
from app.utils.exceptions import BookingServiceError, ValidationError

logger = get_logger(__name__)
router = APIRouter(prefix="/bookings")
settings = get_settings()


@router.post("/", status_code=201)
async def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db)
) -> Union[BookingConfirmation, DuplicateBookingError, MinimumTimeframeError, ValidationErrorResponse, ServiceErrorResponse]:
    """
    Create a new booking inquiry with enhanced error handling.
    
    This endpoint handles the submission of event booking inquiries from the frontend.
    It validates the data, creates the booking record, and sends confirmation emails.
    
    Returns different response models based on the outcome:
    - BookingSuccessResponse: On successful creation
    - DuplicateBookingError: When a booking already exists for the same email/date
    - MinimumTimeframeError: When booking doesn't meet minimum advance notice
    - ValidationErrorResponse: For field validation errors
    - ServiceErrorResponse: For technical/service errors
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
        # Handle different types of validation errors
        if e.error_code == "DUPLICATE_BOOKING":
            # Properly format duplicate booking error
            error_details = e.details.copy()
            # Fix datetime serialization
            if 'timestamp' in error_details:
                error_details['timestamp'] = datetime.utcnow().isoformat()
            
            if 'message' not in error_details:
                error_details['message'] = e.message
            
            raise HTTPException(
                status_code=409,  # Use 409 for duplicate resource
                detail=error_details
            )
        else:
            # Handle other validation errors
            raise HTTPException(
                status_code=422,
                detail={
                    "status": "error",
                    "message": e.message,
                    "error_code": e.error_code,
                    "validation_errors": [
                        {
                            "field": e.details.get("field", "unknown"),
                            "message": e.message,
                            "type": e.error_code
                        }
                    ],
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
    
    except BookingServiceError as e:
        # Handle service-specific errors
        reference_id = str(uuid.uuid4())[:8]
        logger.error(f"Booking service error [{reference_id}]: {e}")
        
        raise HTTPException(
            status_code=500,
            detail=ServiceErrorResponse(
                message="We're experiencing technical difficulties. Please try again or contact us directly.",
                error_code="SERVICE_ERROR",
                reference_id=reference_id,
                contact_info=ContactInfo(
                    email=getattr(settings, 'BUSINESS_EMAIL', 'info@business.com'),
                    phone=getattr(settings, 'BUSINESS_PHONE', None)
                ),
                retry_after=30
            ).dict()
        )
    
    except Exception as e:
        # Handle unexpected errors
        reference_id = str(uuid.uuid4())[:8]
        logger.error(f"Unexpected booking error [{reference_id}]: {e}", exc_info=True)
        
        raise HTTPException(
            status_code=500,
            detail=ServiceErrorResponse(
                message="An unexpected error occurred. Our team has been notified. Please contact us directly or try again later.",
                error_code="SYSTEM_ERROR",
                reference_id=reference_id,
                contact_info=ContactInfo(
                    email=getattr(settings, 'BUSINESS_EMAIL', 'info@business.com'),
                    phone=getattr(settings, 'BUSINESS_PHONE', None)
                )
            ).dict()
        )


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
                description="Baby showers and welcoming celebrations"
            ),
            EventTypeOption(
                value=EventType.GENDER_REVEAL.value,
                label="Gender Reveal",
                description="Gender reveal parties and announcements"
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
        
        # Service options (matching your existing services)
        services = [
            ServiceOption(
                id="led-numbers",
                name="4FT LED Number Hire",
                description="Illuminated LED numbers for birthdays, anniversaries, and celebrations.",
                base_price=50.00,
                is_popular=True
            ),
            ServiceOption(
                id="birthday-package",
                name="Birthday Package",
                description="Complete birthday setup with LED numbers, balloon arch, shimmer wall, neon sign and more.",
                base_price=230.00,
                is_popular=True
            ),
            ServiceOption(
                id="baby-shower-package",
                name="Baby Shower Package",
                description="Celebrate new arrivals with a magical themed display including BABY balloon boxes and teddy.",
                base_price=250.00,
                is_popular=False
            ),
            ServiceOption(
                id="gender-reveal-package",
                name="Gender Reveal Package",
                description="Stylish setup for gender reveal parties with backdrop, neon sign and balloons.",
                base_price=230.00,
                is_popular=False
            ),
            ServiceOption(
                id="christening-package",
                name="Christening Package",
                description="Elegant setup for christening celebrations with a soft, welcoming theme.",
                base_price=180.00,
                is_popular=False
            ),
            ServiceOption(
                id="wedding-package",
                name="Wedding Package",
                description="Elegant wedding package with floral displays, shimmer walls, neon sign and balloon arch.",
                base_price=250.00,
                is_popular=True
            ),
            ServiceOption(
                id="engagement-package",
                name="Engagement Package",
                description="Celebrate engagements with a romantic backdrop, neon lighting, flowers and balloons.",
                base_price=250.00,
                is_popular=False
            ),
            ServiceOption(
                id="retirement-package",
                name="Retirement Package",
                description="Send off in style with a full event backdrop, neon lighting, flowers and balloons.",
                base_price=250.00,
                is_popular=False
            ),
            ServiceOption(
                id="anniversary-package",
                name="Anniversary Package",
                description="Celebrate anniversaries with LED numbers, balloons, flowers and a neon backdrop.",
                base_price=250.00,
                is_popular=False
            ),
            ServiceOption(
                id="custom-signs",
                name="Customised Wooden Signs",
                description="Personalised wooden signs created with precision laser cutting technology.",
                base_price=30.00,
                is_popular=False
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
            "Indoor Venue", "Outdoor Venue", "Garden", "Marquee", "Church", "Village Hall", 
            "Hotel", "Restaurant", "Private Residence", "Community Centre", 
            "Barn", "Country House", "Registry Office", "Other"
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
            min_advance_days=0  # Set to 0 as requested (no minimum timeframe)
        )
        
    except Exception as e:
        logger.error(f"Error fetching form options: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch form options")