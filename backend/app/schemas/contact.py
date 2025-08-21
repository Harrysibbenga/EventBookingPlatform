"""
Pydantic schemas for contact form data validation and serialization.
Defines request/response models for the contact API endpoints.
"""

from pydantic import BaseModel, EmailStr, validator, Field, HttpUrl
from typing import Optional, List
from datetime import datetime

from app.models.contact import ContactType, ContactStatus, ContactPriority


class ContactBase(BaseModel):
    """Base contact schema with common fields."""
    
    # Contact information
    name: str = Field(..., min_length=2, max_length=100, description="Contact person's full name")
    email: EmailStr = Field(..., description="Contact email address")
    phone: Optional[str] = Field(None, regex=r"^[\+]?[1-9][\d\s\-\(\)]{7,15}$", description="Contact phone number")
    company: Optional[str] = Field(None, max_length=200, description="Company name")
    website: Optional[HttpUrl] = Field(None, description="Website URL")
    
    # Inquiry details
    subject: str = Field(..., min_length=5, max_length=200, description="Inquiry subject")
    message: str = Field(..., min_length=10, max_length=2000, description="Inquiry message")
    contact_type: ContactType = Field(ContactType.GENERAL, description="Type of inquiry")
    
    # Preferences
    preferred_contact_time: Optional[str] = Field(None, max_length=100, description="Preferred contact time")
    timezone: Optional[str] = Field(None, max_length=50, description="Timezone")
    
    # Marketing and source tracking
    source: Optional[str] = Field(None, max_length=100, description="How they heard about us")
    is_newsletter_signup: bool = Field(False, description="Newsletter subscription consent")
    
    @validator("name")
    def validate_name(cls, v):
        """Validate contact name format."""
        if not v.replace(" ", "").replace("-", "").replace("'", "").replace(".", "").isalpha():
            raise ValueError("Name must contain only letters, spaces, hyphens, apostrophes, and periods")
        return v.title()
    
    @validator("subject")
    def validate_subject(cls, v):
        """Validate subject line."""
        # Check for common spam patterns
        spam_keywords = ["lottery", "winner", "million", "inheritance", "viagra", "casino"]
        if any(keyword in v.lower() for keyword in spam_keywords):
            raise ValueError("Subject contains prohibited content")
        return v.strip()
    
    @validator("message")
    def validate_message(cls, v):
        """Validate message content."""
        # Basic spam detection
        if v.count("http") > 3:  # Too many links
            raise ValueError("Message contains too many links")
        
        # Check for excessive capitalization
        if sum(1 for c in v if c.isupper()) > len(v) * 0.5:
            raise ValueError("Message contains excessive capitalization")
        
        return v.strip()


class ContactCreate(ContactBase):
    """Schema for creating a new contact inquiry."""
    
    # Terms and consent
    terms_accepted: bool = Field(True, description="Terms and conditions acceptance")
    privacy_consent: bool = Field(True, description="Privacy policy consent")
    
    # Metadata (typically populated by frontend)
    referrer_url: Optional[str] = Field(None, max_length=500, description="Referring page URL")
    user_agent: Optional[str] = Field(None, max_length=500, description="Browser user agent")
    
    @validator("terms_accepted")
    def validate_terms(cls, v):
        """Ensure terms are accepted."""
        if not v:
            raise ValueError("Terms and conditions must be accepted")
        return v
    
    @validator("privacy_consent")
    def validate_privacy(cls, v):
        """Ensure privacy consent is given."""
        if not v:
            raise ValueError("Privacy policy consent must be given")
        return v


class ContactUpdate(BaseModel):
    """Schema for updating contact inquiries (admin use)."""
    
    # Admin-only fields
    status: Optional[ContactStatus] = None
    priority: Optional[ContactPriority] = None
    admin_notes: Optional[str] = Field(None, max_length=2000)
    requires_follow_up: Optional[bool] = None
    is_spam: Optional[bool] = None
    
    # Response tracking
    replied_at: Optional[datetime] = None
    read_at: Optional[datetime] = None


class ContactResponse(ContactBase):
    """Schema for contact inquiry responses."""
    
    id: int
    status: ContactStatus
    priority: ContactPriority
    requires_follow_up: bool
    is_spam: bool
    created_at: datetime
    updated_at: Optional[datetime]
    replied_at: Optional[datetime]
    read_at: Optional[datetime]
    
    # Admin fields (only shown to admin users)
    admin_notes: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    referrer_url: Optional[str] = None
    
    class Config:
        orm_mode = True
        use_enum_values = True


class ContactList(BaseModel):
    """Schema for paginated contact list responses."""
    
    contacts: List[ContactResponse]
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool


class ContactStats(BaseModel):
    """Schema for contact inquiry statistics."""
    
    total_contacts: int
    new_contacts: int
    pending_replies: int
    this_month_contacts: int
    avg_response_time_hours: float
    contact_types_breakdown: List[dict]
    monthly_trends: List[dict]
    top_sources: List[dict]


class ContactFilter(BaseModel):
    """Schema for filtering contact inquiries."""
    
    status: Optional[ContactStatus] = None
    contact_type: Optional[ContactType] = None
    priority: Optional[ContactPriority] = None
    is_spam: Optional[bool] = None
    requires_follow_up: Optional[bool] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    source: Optional[str] = None
    search: Optional[str] = Field(None, max_length=100, description="Search in name, email, subject, or message")


class ContactConfirmation(BaseModel):
    """Schema for contact form confirmation response."""
    
    success: bool
    contact_id: int
    message: str
    reference_number: str
    estimated_response_time: str


class ContactReply(BaseModel):
    """Schema for admin reply to contact inquiry."""
    
    subject: str = Field(..., min_length=5, max_length=200)
    message: str = Field(..., min_length=10, max_length=5000)
    cc_admin: bool = Field(False, description="Copy admin on reply")
    mark_as_resolved: bool = Field(True, description="Mark inquiry as resolved")


class ContactTemplate(BaseModel):
    """Schema for email response templates."""
    
    id: str
    name: str
    subject: str
    message: str
    contact_type: Optional[ContactType] = None
    is_active: bool = True


class ContactFormOptions(BaseModel):
    """Schema for contact form configuration options."""
    
    contact_types: List[dict]
    sources: List[str]
    timezones: List[dict]
    preferred_times: List[str]
    max_message_length: int = 2000


class AutoReply(BaseModel):
    """Schema for automated reply configuration."""
    
    enabled: bool
    subject: str
    message: str
    delay_minutes: int = 0
    contact_types: List[ContactType] = []


class SpamFilter(BaseModel):
    """Schema for spam filtering configuration."""
    
    enabled: bool
    keywords: List[str]
    max_links: int = 3
    min_message_length: int = 10
    check_ip_reputation: bool = True
    require_human_verification: bool = False