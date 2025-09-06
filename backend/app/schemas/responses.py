# app/schemas/responses.py
"""
Enhanced response models for booking and contact APIs.
Provides structured error handling and user guidance.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, date
from decimal import Decimal
from enum import Enum

from app.models.booking import BookingStatus, EventType, ContactMethod


class ResponseStatus(str, Enum):
    """Standard response status codes."""
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ContactInfo(BaseModel):
    """Contact information for user assistance."""
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    business_hours: Optional[str] = "Monday-Friday, 9 AM - 6 PM"


class UserAction(BaseModel):
    """Suggested user actions with clear labels."""
    text: str = Field(..., description="Action button text")
    action_type: str = Field(..., description="Type of action (email, phone, link, retry)")
    url: Optional[str] = Field(None, description="URL for link actions")
    phone: Optional[str] = Field(None, description="Phone number for call actions")
    email: Optional[str] = Field(None, description="Email address for email actions")
    is_primary: bool = Field(False, description="Whether this is the primary action")


class Timeline(BaseModel):
    """Expected timeline for booking process."""
    confirmation_email: str = "Within 5 minutes"
    initial_contact: str = "Within 24 hours"
    detailed_quote: str = "Within 2-3 business days"
    booking_confirmation: str = "Upon approval"

# ==================== ERROR RESPONSE MODELS ====================

class DuplicateBookingError(BaseModel):
    """Specific error response for duplicate booking attempts."""
    status: ResponseStatus = ResponseStatus.ERROR
    message: str
    error_code: str = "DUPLICATE_BOOKING"
    existing_booking: Dict[str, Any] = Field(
        description="Information about the existing booking"
    )
    user_actions: List[UserAction] = Field(
        description="Suggested actions for the user"
    )
    contact_info: ContactInfo
    recommendations: List[str] = Field(
        description="Specific recommendations based on booking status"
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        schema_extra = {
            "example": {
                "status": "error",
                "message": "We already have a booking inquiry from you for March 15, 2025. Your inquiry (Reference: BK001234) is currently being processed by our team.",
                "error_code": "DUPLICATE_BOOKING",
                "existing_booking": {
                    "id": 1234,
                    "reference_number": "BK001234",
                    "status": "contacted",
                    "event_date": "2025-03-15",
                    "created_at": "2025-01-10T10:30:00Z",
                    "time_since_booking": "2 hours ago"
                },
                "user_actions": [
                    {
                        "text": "Check Email",
                        "action_type": "email",
                        "email": "user@email.com",
                        "is_primary": True
                    },
                    {
                        "text": "Call Us",
                        "action_type": "phone",
                        "phone": "(555) 123-4567",
                        "is_primary": False
                    }
                ],
                "contact_info": {
                    "email": "events@company.com",
                    "phone": "(555) 123-4567"
                },
                "recommendations": [
                    "Check your email (including spam folder) for our updates",
                    "We should have a detailed quote for you soon",
                    "If you haven't heard from us in 48 hours, please give us a call"
                ]
            }
        }


class MinimumTimeframeError(BaseModel):
    """Error response for bookings with insufficient advance notice."""
    status: ResponseStatus = ResponseStatus.ERROR
    message: str
    error_code: str = "MINIMUM_TIMEFRAME_ERROR"
    minimum_days: int = Field(description="Minimum required advance notice in days")
    days_until_event: int = Field(description="Days between today and event date")
    rush_booking_available: bool = Field(description="Whether rush booking is possible")
    user_actions: List[UserAction] = Field(description="Available options for the user")
    contact_info: ContactInfo
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        schema_extra = {
            "example": {
                "status": "error",
                "message": "For events with more than 50 guests, we typically need at least 7 days notice. Please call us directly to discuss rush booking options.",
                "error_code": "MINIMUM_TIMEFRAME_ERROR",
                "minimum_days": 7,
                "days_until_event": 3,
                "rush_booking_available": True,
                "user_actions": [
                    {
                        "text": "Call for Rush Booking",
                        "action_type": "phone",
                        "phone": "(555) 123-4567",
                        "is_primary": True
                    },
                    {
                        "text": "Choose Different Date",
                        "action_type": "retry",
                        "is_primary": False
                    }
                ],
                "contact_info": {
                    "email": "events@company.com",
                    "phone": "(555) 123-4567"
                }
            }
        }


class ValidationErrorResponse(BaseModel):
    """Detailed validation error response."""
    status: ResponseStatus = ResponseStatus.ERROR
    message: str = "Please correct the following errors and try again"
    error_code: str = "VALIDATION_ERROR"
    validation_errors: List[Dict[str, Any]] = Field(
        description="Detailed validation errors"
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        schema_extra = {
            "example": {
                "status": "error",
                "message": "Please correct the following errors and try again",
                "error_code": "VALIDATION_ERROR",
                "validation_errors": [
                    {
                        "field": "contact_email",
                        "message": "Please enter a valid email address",
                        "type": "format_error"
                    },
                    {
                        "field": "guest_count",
                        "message": "Guest count must be at least 1",
                        "type": "min_value_error"
                    }
                ]
            }
        }


class ServiceErrorResponse(BaseModel):
    """Response for service-level errors."""
    status: ResponseStatus = ResponseStatus.ERROR
    message: str = "We're experiencing technical difficulties. Please try again or contact us directly."
    error_code: str = "SERVICE_ERROR"
    reference_id: str = Field(description="Reference ID for tracking this error")
    contact_info: ContactInfo
    retry_after: Optional[int] = Field(None, description="Suggested retry delay in seconds")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ==================== STANDARD RESPONSE MODELS ====================

class BookingStandardResponse(BaseModel):
    """Standard booking data response for listings."""
    id: int
    event_type: str
    event_date: date
    event_time: Optional[str]
    guest_count: int
    venue_name: Optional[str]
    status: str
    contact_name: str
    contact_email: str
    reference_number: str
    created_at: datetime
    is_priority: bool
    
    # Admin-only fields (conditionally included)
    admin_notes: Optional[str] = None
    estimated_quote: Optional[Decimal] = None
    
    class Config:
        orm_mode = True


# ==================== UTILITY FUNCTIONS ====================

def create_duplicate_booking_response(
    existing_booking: Any,
    business_email: str,
    business_phone: Optional[str] = None
) -> DuplicateBookingError:
    """Create a comprehensive duplicate booking error response."""
    
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
    
    # Generate reference number
    reference_number = f"BK{existing_booking.id:06d}"
    
    # Status-specific messages and actions
    status_messages = {
        BookingStatus.PENDING: {
            "message": f"""We already have a booking inquiry from you for {existing_booking.event_date.strftime('%B %d, %Y')}.

Your inquiry (Reference: {reference_number}) was submitted {time_text} and is currently under review.

What to do next:
• Check your email for our confirmation message
• We typically respond within 24 hours
• If you need to make changes, please reply to our confirmation email
• For urgent matters, contact us directly

Need to modify your request? Contact us directly instead of submitting again.""",
            "recommendations": [
                "Check your email (including spam folder) for our confirmation",
                "If urgent, call us directly rather than submitting again",
                "We respond to all inquiries within 24 hours during business days"
            ]
        },
        BookingStatus.CONTACTED: {
            "message": f"""Great news! We're already working on your booking inquiry for {existing_booking.event_date.strftime('%B %d, %Y')}.

Your inquiry (Reference: {reference_number}) is currently being processed by our team.

What to expect:
• We should have a detailed quote for you soon
• Check your email for updates from our team
• If you haven't heard from us in 48 hours, please give us a call

Need to add or change something? Reply to our last email or call us directly.""",
            "recommendations": [
                "Look for our follow-up email with next steps",
                "If you have additional requirements, reply to our email",
                "We'll send you a detailed quote within 2-3 business days"
            ]
        },
        BookingStatus.QUOTED: {
            "message": f"""We've already sent you a quote for your event on {existing_booking.event_date.strftime('%B %d, %Y')}!

Your inquiry (Reference: {reference_number}) has been quoted and is awaiting your response.

Next steps:
• Check your email for our detailed quote
• Review the proposal and let us know if you'd like to proceed
• If you need modifications, reply to our quote email
• Ready to book? Follow the confirmation instructions in your quote

Can't find our quote email? Contact us and we'll resend it immediately.""",
            "recommendations": [
                "Review the quote we sent to your email",
                "Contact us if you need any modifications",
                "Confirm your booking by following the quote instructions",
                "Quote is valid for 30 days from the send date"
            ]
        },
        BookingStatus.CONFIRMED: {
            "message": f"""Wonderful! Your event on {existing_booking.event_date.strftime('%B %d, %Y')} is already confirmed.

Your booking (Reference: {reference_number}) is all set!

What's next:
• You should have received a confirmation email with all details
• We'll be in touch closer to your event date with final details
• Need to make changes? Contact us directly

Looking forward to making your event amazing!""",
            "recommendations": [
                "Your event is confirmed - no further action needed",
                "We'll contact you 2 weeks before your event with final details",
                "Any changes should be communicated directly to us",
                "Thank you for choosing us for your special event!"
            ]
        }
    }
    
    # Get status-specific content
    status_info = status_messages.get(
        existing_booking.status, 
        status_messages[BookingStatus.PENDING]
    )
    
    # Create user actions
    user_actions = [
        UserAction(
            text="Check Email",
            action_type="email",
            email=existing_booking.contact_email,
            is_primary=True
        ),
        UserAction(
            text="Call Us",
            action_type="phone",
            phone=business_phone,
            is_primary=False
        )
    ]
    
    # Add status-specific actions
    if existing_booking.status == BookingStatus.QUOTED:
        user_actions.insert(0, UserAction(
            text="Review Quote",
            action_type="email",
            email=existing_booking.contact_email,
            is_primary=True
        ))
    
    return DuplicateBookingError(
        message=status_info["message"],
        existing_booking={
            "id": existing_booking.id,
            "reference_number": reference_number,
            "status": existing_booking.status.value,
            "event_date": existing_booking.event_date.isoformat(),
            "event_type": existing_booking.event_type.value,
            "created_at": existing_booking.created_at.isoformat(),
            "time_since_booking": time_text
        },
        user_actions=user_actions,
        contact_info=ContactInfo(
            email=business_email,
            phone=business_phone
        ),
        recommendations=status_info["recommendations"]
    )


def create_minimum_timeframe_response(
    days_until_event: int,
    minimum_days: int,
    guest_count: int,
    business_email: str,
    business_phone: Optional[str] = None
) -> MinimumTimeframeError:
    """Create minimum timeframe error response."""
    
    rush_available = guest_count <= 50 or days_until_event >= 3
    
    if guest_count > 50:
        message = f"For events with more than 50 guests, we typically need at least {minimum_days} days notice. Please call us directly to discuss rush booking options."
    else:
        message = f"We typically need at least {minimum_days} days notice for bookings. Please call us to discuss your timeline or choose a later date."
    
    user_actions = []
    
    if rush_available:
        user_actions.append(UserAction(
            text="Call for Rush Booking",
            action_type="phone",
            phone=business_phone,
            is_primary=True
        ))
    
    user_actions.extend([
        UserAction(
            text="Choose Different Date",
            action_type="retry",
            is_primary=False
        ),
        UserAction(
            text="Email Us",
            action_type="email",
            email=business_email,
            is_primary=False
        )
    ])
    
    return MinimumTimeframeError(
        message=message,
        minimum_days=minimum_days,
        days_until_event=days_until_event,
        rush_booking_available=rush_available,
        user_actions=user_actions,
        contact_info=ContactInfo(
            email=business_email,
            phone=business_phone
        )
    )