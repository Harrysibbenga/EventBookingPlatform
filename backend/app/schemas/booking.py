"""
Pydantic schemas for booking data validation and serialization.
Defines request/response models for the booking API endpoints.
"""

from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List
from datetime import datetime, date, time
from decimal import Decimal

from app.models.booking import EventType, BookingStatus, ContactMethod


class BookingBase(BaseModel):
    """Base booking schema with common fields."""
    
    # Event details
    event_type: EventType
    event_date: date = Field(..., description="Event date")
    event_time: Optional[str] = Field(None, pattern=r"^(0?[1-9]|1[0-2]):[0-5][0-9]\s?(AM|PM)$", description="Event time in HH:MM AM/PM format")
    duration_hours: Optional[int] = Field(4, ge=1, le=24, description="Event duration in hours")
    guest_count: int = Field(..., ge=1, le=10000, description="Number of expected guests")
    
    # Venue information
    venue_name: Optional[str] = Field(None, max_length=200)
    venue_address: Optional[str] = Field(None, max_length=500)
    venue_type: Optional[str] = Field(None, max_length=100)
    
    # Budget information
    budget_min: Optional[Decimal] = Field(None, ge=0, description="Minimum budget")
    budget_max: Optional[Decimal] = Field(None, ge=0, description="Maximum budget")
    budget_flexible: bool = Field(True, description="Whether budget is flexible")
    
    # Services and requirements
    services_needed: Optional[str] = Field(None, max_length=1000, description="Requested services")
    service_package_id: Optional[str] = Field(None, description="Service package ID if applicable")
    special_requirements: Optional[str] = Field(None, max_length=1000, description="Special requirements or notes")
    dietary_restrictions: Optional[str] = Field(None, max_length=500)
    accessibility_needs: Optional[str] = Field(None, max_length=500)
    
    # Contact information
    contact_name: str = Field(..., min_length=2, max_length=100, description="Contact person's full name")
    contact_email: EmailStr = Field(..., description="Contact email address")
    contact_phone: Optional[str] = Field(None, pattern=r"^[\+]?[1-9][\d\s\-\(\)]{7,15}$", description="Contact phone number")
    preferred_contact: ContactMethod = Field(ContactMethod.EMAIL, description="Preferred contact method")
    
    # Additional information
    how_heard_about_us: Optional[str] = Field(None, max_length=100)
    previous_client: bool = Field(False, description="Whether client has booked before")
    
    @validator("budget_max")
    def validate_budget_range(cls, v, values):
        """Ensure max budget is greater than min budget."""
        if v is not None and "budget_min" in values and values["budget_min"] is not None:
            if v < values["budget_min"]:
                raise ValueError("Maximum budget must be greater than minimum budget")
        return v
    
    @validator("event_date")
    def validate_event_date(cls, v):
        """Ensure event date is not in the past."""
        if v < date.today():
            raise ValueError("Event date cannot be in the past")
        return v
    
    @validator("contact_name")
    def validate_contact_name(cls, v):
        """Validate contact name format."""
        if not v.replace(" ", "").replace("-", "").replace("'", "").isalpha():
            raise ValueError("Contact name must contain only letters, spaces, hyphens, and apostrophes")
        return v.title()


class BookingCreate(BookingBase):
    """Schema for creating a new booking inquiry."""
    
    # Optional fields for enhanced data collection
    marketing_consent: bool = Field(False, description="Consent to receive marketing communications")
    terms_accepted: bool = Field(True, description="Terms and conditions acceptance")
    
    @validator("terms_accepted")
    def validate_terms(cls, v):
        """Ensure terms are accepted."""
        if not v:
            raise ValueError("Terms and conditions must be accepted")
        return v


class BookingUpdate(BaseModel):
    """Schema for updating booking inquiries (admin use)."""
    
    # Admin-only fields
    status: Optional[BookingStatus] = None
    admin_notes: Optional[str] = Field(None, max_length=2000)
    estimated_quote: Optional[Decimal] = Field(None, ge=0)
    follow_up_date: Optional[datetime] = None
    is_priority: Optional[bool] = None
    is_archived: Optional[bool] = None
    requires_consultation: Optional[bool] = None
    contacted_at: Optional[datetime] = None
    quoted_at: Optional[datetime] = None


class BookingResponse(BookingBase):
    """Schema for booking inquiry responses."""
    
    id: int
    status: BookingStatus
    is_priority: bool
    is_archived: bool
    requires_consultation: bool
    created_at: datetime
    updated_at: Optional[datetime]
    contacted_at: Optional[datetime]
    quoted_at: Optional[datetime]
    
    # Admin fields (only shown to admin users)
    admin_notes: Optional[str] = None
    estimated_quote: Optional[Decimal] = None
    follow_up_date: Optional[datetime] = None
    
    class Config:
        orm_mode = True
        use_enum_values = True


class BookingList(BaseModel):
    """Schema for paginated booking list responses."""
    
    bookings: List[BookingResponse]
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool


class BookingStats(BaseModel):
    """Schema for booking statistics."""
    
    total_bookings: int
    pending_bookings: int
    this_month_bookings: int
    priority_bookings: int
    avg_guest_count: float
    popular_event_types: List[dict]
    monthly_trends: List[dict]


class BookingFilter(BaseModel):
    """Schema for filtering booking inquiries."""
    
    status: Optional[BookingStatus] = None
    event_type: Optional[EventType] = None
    is_priority: Optional[bool] = None
    is_archived: Optional[bool] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    guest_count_min: Optional[int] = Field(None, ge=1)
    guest_count_max: Optional[int] = Field(None, le=10000)
    budget_min: Optional[Decimal] = Field(None, ge=0)
    budget_max: Optional[Decimal] = Field(None, ge=0)
    search: Optional[str] = Field(None, max_length=100, description="Search in name, email, or notes")


class BookingConfirmation(BaseModel):
    """Schema for booking confirmation response."""
    
    success: bool
    booking_id: int
    message: str
    confirmation_number: str
    next_steps: List[str]


# Utility schemas for form options
class EventTypeOption(BaseModel):
    """Schema for event type options."""
    value: str
    label: str
    description: Optional[str] = None


class ServiceOption(BaseModel):
    """Schema for service options."""
    id: str
    name: str
    description: Optional[str] = None
    base_price: Optional[Decimal] = None
    is_popular: bool = False


class BookingFormOptions(BaseModel):
    """Schema for booking form configuration options."""
    
    event_types: List[EventTypeOption]
    services: List[ServiceOption]
    contact_methods: List[dict]
    venue_types: List[str]
    time_slots: List[str]
    max_guest_count: int = 1000
    min_advance_days: int = 7