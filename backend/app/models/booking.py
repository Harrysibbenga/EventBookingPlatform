"""
Booking database model for storing event booking inquiries.
Defines the database schema and relationships for booking data.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Boolean, Numeric
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum as PyEnum

from app.core.database import Base


class EventType(PyEnum):
    """Enumeration of supported event types."""
    WEDDING = "wedding"
    BIRTHDAY = "birthday"
    CORPORATE = "corporate"
    ANNIVERSARY = "anniversary"
    GRADUATION = "graduation"
    BABY_SHOWER = "baby_shower"
    GENDER_REVEAL = "gender_reveal"
    PROPOSAL="proposal"
    ENGAGEMENT = "engagement"
    RETIREMENT = "retirement"
    HOLIDAY = "holiday"
    OTHER = "other"


class BookingStatus(PyEnum):
    """Enumeration of booking inquiry statuses."""
    PENDING = "pending"
    REVIEWED = "reviewed"
    CONTACTED = "contacted"
    QUOTED = "quoted"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class ContactMethod(PyEnum):
    """Preferred contact method enumeration."""
    EMAIL = "email"
    PHONE = "phone"
    EITHER = "either"


class Booking(Base):
    """
    Booking model for storing event booking inquiries.
    
    Attributes:
        id: Primary key
        event_type: Type of event being booked
        event_date: Preferred event date
        event_time: Preferred event time
        duration_hours: Expected event duration
        guest_count: Number of expected guests
        venue_name: Event venue name
        venue_address: Event venue address
        budget_min: Minimum budget range
        budget_max: Maximum budget range
        services_needed: List of requested services
        special_requirements: Additional requirements/notes
        contact_name: Client contact name
        contact_email: Client email address
        contact_phone: Client phone number
        preferred_contact: Preferred contact method
        status: Current inquiry status
        admin_notes: Internal admin notes
        created_at: Record creation timestamp
        updated_at: Record update timestamp
        contacted_at: When client was contacted
        is_priority: Priority flag for important inquiries
    """
    
    __tablename__ = "bookings"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Event details
    event_type = Column(Enum(EventType), nullable=False)
    event_date = Column(DateTime, nullable=False)
    event_time = Column(String(10))  # Format: "HH:MM AM/PM"
    duration_hours = Column(Integer, default=4)
    guest_count = Column(Integer, nullable=False)
    
    # Venue information
    venue_name = Column(String(200))
    venue_address = Column(Text)
    venue_type = Column(String(100))  # Indoor, Outdoor, Church, etc.
    
    # Budget information
    budget_min = Column(Numeric(10, 2))
    budget_max = Column(Numeric(10, 2))
    budget_flexible = Column(Boolean, default=True)
    
    # Services and requirements
    services_needed = Column(Text)  # JSON string of requested services
    service_package_id = Column(Integer)  # Foreign key to service package if applicable
    special_requirements = Column(Text)
    dietary_restrictions = Column(Text)
    accessibility_needs = Column(Text)
    
    # Contact information
    contact_name = Column(String(100), nullable=False)
    contact_email = Column(String(255), nullable=False, index=True)
    contact_phone = Column(String(20))
    preferred_contact = Column(Enum(ContactMethod), default=ContactMethod.EMAIL)
    
    # Additional client info
    how_heard_about_us = Column(String(100))
    previous_client = Column(Boolean, default=False)
    
    # Status and admin fields
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING, index=True)
    admin_notes = Column(Text)
    estimated_quote = Column(Numeric(10, 2))
    follow_up_date = Column(DateTime)
    
    # Priority and flags
    is_priority = Column(Boolean, default=False, index=True)
    is_archived = Column(Boolean, default=False, index=True)
    requires_consultation = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    contacted_at = Column(DateTime(timezone=True))
    quoted_at = Column(DateTime(timezone=True))
    
    def __repr__(self):
        return f"<Booking(id={self.id}, type={self.event_type.value}, client={self.contact_name})>"
    
    @property
    def is_recent(self) -> bool:
        """Check if booking was created in the last 24 hours."""
        if not self.created_at:
            return False
        return (datetime.utcnow() - self.created_at).days < 1
    
    @property
    def is_urgent(self) -> bool:
        """Check if event date is approaching (within 30 days)."""
        if not self.event_date:
            return False
        # FIXED: Convert event_date to datetime for proper comparison
        event_datetime = datetime.combine(self.event_date, datetime.min.time())
        return (event_datetime - datetime.utcnow()).days <= 30
    
    @property
    def estimated_budget(self) -> float:
        """Get estimated budget midpoint."""
        if self.budget_min and self.budget_max:
            return float((self.budget_min + self.budget_max) / 2)
        elif self.budget_min:
            return float(self.budget_min)
        elif self.budget_max:
            return float(self.budget_max)
        return 0.0
    
    def to_dict(self) -> dict:
        """Convert booking to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "event_type": self.event_type.value if self.event_type else None,
            "event_date": self.event_date.isoformat() if self.event_date else None,
            "event_time": self.event_time,
            "duration_hours": self.duration_hours,
            "guest_count": self.guest_count,
            "venue_name": self.venue_name,
            "venue_address": self.venue_address,
            "venue_type": self.venue_type,
            "budget_min": float(self.budget_min) if self.budget_min else None,
            "budget_max": float(self.budget_max) if self.budget_max else None,
            "budget_flexible": self.budget_flexible,
            "services_needed": self.services_needed,
            "special_requirements": self.special_requirements,
            "contact_name": self.contact_name,
            "contact_email": self.contact_email,
            "contact_phone": self.contact_phone,
            "preferred_contact": self.preferred_contact.value if self.preferred_contact else None,
            "status": self.status.value if self.status else None,
            "is_priority": self.is_priority,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }