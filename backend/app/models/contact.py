"""
Contact database model for storing general contact form submissions.
Handles inquiries that are not specific booking requests.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Boolean
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum as PyEnum

from app.core.database import Base


class ContactType(PyEnum):
    """Enumeration of contact inquiry types."""
    GENERAL = "general"
    PRICING = "pricing"
    AVAILABILITY = "availability"
    SERVICES = "services"
    PARTNERSHIP = "partnership"
    FEEDBACK = "feedback"
    COMPLAINT = "complaint"
    OTHER = "other"


class ContactStatus(PyEnum):
    """Enumeration of contact inquiry statuses."""
    NEW = "new"
    READ = "read"
    REPLIED = "replied"
    RESOLVED = "resolved"
    ARCHIVED = "archived"


class ContactPriority(PyEnum):
    """Contact inquiry priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class Contact(Base):
    """
    Contact model for storing general contact form submissions.
    
    Attributes:
        id: Primary key
        name: Contact person's name
        email: Contact email address
        phone: Contact phone number
        subject: Inquiry subject line
        message: Inquiry message content
        contact_type: Type of inquiry
        company: Company name (optional)
        website: Website URL (optional)
        preferred_contact_time: When to contact them
        status: Current inquiry status
        priority: Inquiry priority level
        admin_notes: Internal admin notes
        replied_at: When inquiry was replied to
        created_at: Record creation timestamp
        updated_at: Record update timestamp
        is_spam: Spam flag
        source: How they found us
    """
    
    __tablename__ = "contacts"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Contact information
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(20))
    company = Column(String(200))
    website = Column(String(255))
    
    # Inquiry details
    subject = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    contact_type = Column(Enum(ContactType), default=ContactType.GENERAL, index=True)
    
    # Scheduling preferences
    preferred_contact_time = Column(String(100))  # e.g., "Weekday mornings"
    timezone = Column(String(50))
    
    # Status and management
    status = Column(Enum(ContactStatus), default=ContactStatus.NEW, index=True)
    priority = Column(Enum(ContactPriority), default=ContactPriority.NORMAL, index=True)
    admin_notes = Column(Text)
    
    # Marketing and analytics
    source = Column(String(100))  # How they heard about us
    referrer_url = Column(String(500))  # Referring page URL
    user_agent = Column(String(500))  # Browser info for analytics
    ip_address = Column(String(45))  # For spam detection
    
    # Flags
    is_spam = Column(Boolean, default=False, index=True)
    is_newsletter_signup = Column(Boolean, default=False)
    requires_follow_up = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    replied_at = Column(DateTime(timezone=True))
    read_at = Column(DateTime(timezone=True))
    
    def __repr__(self):
        return f"<Contact(id={self.id}, name={self.name}, type={self.contact_type.value})>"
    
    @property
    def is_recent(self) -> bool:
        """Check if contact was created in the last 24 hours."""
        if not self.created_at:
            return False
        return (datetime.utcnow() - self.created_at).days < 1
    
    @property
    def needs_response(self) -> bool:
        """Check if contact needs a response."""
        return self.status in [ContactStatus.NEW, ContactStatus.READ] and not self.is_spam
    
    @property
    def response_time_hours(self) -> float:
        """Calculate hours since inquiry was created."""
        if not self.created_at:
            return 0
        delta = datetime.utcnow() - self.created_at
        return delta.total_seconds() / 3600
    
    @property
    def is_overdue(self) -> bool:
        """Check if response is overdue (>24 hours for normal, >4 hours for urgent)."""
        if self.status in [ContactStatus.REPLIED, ContactStatus.RESOLVED]:
            return False
        
        threshold_hours = 4 if self.priority == ContactPriority.URGENT else 24
        return self.response_time_hours > threshold_hours
    
    def mark_as_read(self):
        """Mark contact as read with timestamp."""
        if self.status == ContactStatus.NEW:
            self.status = ContactStatus.READ
            self.read_at = datetime.utcnow()
    
    def mark_as_replied(self):
        """Mark contact as replied with timestamp."""
        self.status = ContactStatus.REPLIED
        self.replied_at = datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert contact to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "company": self.company,
            "website": self.website,
            "subject": self.subject,
            "message": self.message,
            "contact_type": self.contact_type.value if self.contact_type else None,
            "preferred_contact_time": self.preferred_contact_time,
            "status": self.status.value if self.status else None,
            "priority": self.priority.value if self.priority else None,
            "source": self.source,
            "is_spam": self.is_spam,
            "requires_follow_up": self.requires_follow_up,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "replied_at": self.replied_at.isoformat() if self.replied_at else None
        }