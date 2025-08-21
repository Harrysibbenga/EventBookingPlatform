"""
Contact service for handling business logic related to contact inquiries.
Provides high-level operations for contact management and processing.
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, asc, func, extract
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
import re

from app.models.contact import Contact, ContactType, ContactStatus, ContactPriority
from app.schemas.contact import ContactCreate, ContactUpdate, ContactFilter, ContactReply
from app.services.email_service import email_service
from app.utils.logger import get_logger
from app.utils.exceptions import ContactServiceError, ValidationError

logger = get_logger(__name__)


class ContactService:
    """Service class for contact-related business logic."""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def create_contact(self, contact_data: ContactCreate) -> Contact:
        """
        Create a new contact inquiry.
        
        Args:
            contact_data: Contact creation data
            
        Returns:
            Contact: Created contact instance
        """
        try:
            # Validate and detect spam
            await self._validate_contact_creation(contact_data)
            is_spam = self._detect_spam(contact_data)
            
            # Determine priority
            priority = self._determine_priority(contact_data)
            
            # Create contact instance
            contact = Contact(
                # Contact information
                name=contact_data.name,
                email=contact_data.email.lower(),
                phone=contact_data.phone,
                company=contact_data.company,
                website=str(contact_data.website) if contact_data.website else None,
                
                # Inquiry details
                subject=contact_data.subject,
                message=contact_data.message,
                contact_type=contact_data.contact_type,
                
                # Preferences
                preferred_contact_time=contact_data.preferred_contact_time,
                timezone=contact_data.timezone,
                
                # Marketing and source tracking
                source=contact_data.source,
                is_newsletter_signup=contact_data.is_newsletter_signup,
                referrer_url=contact_data.referrer_url,
                user_agent=contact_data.user_agent,
                
                # Set initial status and flags
                status=ContactStatus.NEW,
                priority=priority,
                is_spam=is_spam,
                requires_follow_up=not is_spam
            )
            
            # Save to database
            self.db.add(contact)
            self.db.commit()
            self.db.refresh(contact)
            
            # Send notifications (only if not spam)
            if not is_spam:
                await self._send_contact_notifications(contact)
            
            logger.info(f"Created contact inquiry {contact.id} from {contact.name}")
            return contact
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to create contact: {e}")
            raise ContactServiceError(f"Failed to create contact: {e}")
    
    def get_contact(self, contact_id: int) -> Optional[Contact]:
        """Get contact by ID."""
        return self.db.query(Contact).filter(Contact.id == contact_id).first()
    
    def get_contacts(
        self,
        filters: Optional[ContactFilter] = None,
        page: int = 1,
        per_page: int = 20,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> Tuple[List[Contact], int]:
        """
        Get paginated list of contacts with optional filtering.
        
        Returns:
            Tuple: (contacts_list, total_count)
        """
        query = self.db.query(Contact)
        
        # Apply filters
        if filters:
            query = self._apply_filters(query, filters)
        
        # Get total count before pagination
        total = query.count()
        
        # Apply sorting
        if hasattr(Contact, sort_by):
            if sort_order.lower() == "desc":
                query = query.order_by(desc(getattr(Contact, sort_by)))
            else:
                query = query.order_by(asc(getattr(Contact, sort_by)))
        
        # Apply pagination
        offset = (page - 1) * per_page
        contacts = query.offset(offset).limit(per_page).all()
        
        return contacts, total
    
    def update_contact(self, contact_id: int, update_data: ContactUpdate) -> Optional[Contact]:
        """Update contact with admin data."""
        contact = self.get_contact(contact_id)
        if not contact:
            return None
        
        # Update fields
        for field, value in update_data.dict(exclude_unset=True).items():
            if hasattr(contact, field):
                setattr(contact, field, value)
        
        # Update timestamp
        contact.updated_at = datetime.utcnow()
        
        # Set specific timestamps based on status changes
        if update_data.status:
            if update_data.status == ContactStatus.REPLIED and not contact.replied_at:
                contact.replied_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(contact)
        
        logger.info(f"Updated contact {contact_id}")
        return contact
    
    def delete_contact(self, contact_id: int) -> bool:
        """Permanently delete contact (typically for spam)."""
        contact = self.get_contact(contact_id)
        if not contact:
            return False
        
        self.db.delete(contact)
        self.db.commit()
        
        logger.info(f"Deleted contact {contact_id}")
        return True
    
    def mark_as_read(self, contact_id: int) -> Optional[Contact]:
        """Mark contact as read."""
        contact = self.get_contact(contact_id)
        if not contact:
            return None
        
        if contact.status == ContactStatus.NEW:
            contact.status = ContactStatus.READ
            contact.read_at = datetime.utcnow()
            contact.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(contact)
        
        return contact
    
    def mark_as_spam(self, contact_id: int, is_spam: bool = True) -> Optional[Contact]:
        """Mark or unmark contact as spam."""
        contact = self.get_contact(contact_id)
        if not contact:
            return None
        
        contact.is_spam = is_spam
        contact.updated_at = datetime.utcnow()
        
        # If marking as spam, set requires_follow_up to False
        if is_spam:
            contact.requires_follow_up = False
        
        self.db.commit()
        self.db.refresh(contact)
        
        logger.info(f"Marked contact {contact_id} as {'spam' if is_spam else 'not spam'}")
        return contact
    
    async def reply_to_contact(self, contact_id: int, reply_data: ContactReply) -> bool:
        """Send a reply to a contact inquiry."""
        contact = self.get_contact(contact_id)
        if not contact:
            return False
        
        try:
            # Send reply email
            await email_service.send_email(
                to_email=contact.email,
                subject=reply_data.subject,
                html_content=reply_data.message,
                cc=[settings.ADMIN_EMAIL] if reply_data.cc_admin else None
            )
            
            # Update contact status
            contact.status = ContactStatus.REPLIED if reply_data.mark_as_resolved else ContactStatus.READ
            contact.replied_at = datetime.utcnow()
            contact.updated_at = datetime.utcnow()
            
            if reply_data.mark_as_resolved:
                contact.status = ContactStatus.RESOLVED
                contact.requires_follow_up = False
            
            self.db.commit()
            
            logger.info(f"Sent reply to contact {contact_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send reply to contact {contact_id}: {e}")
            return False
    
    def get_contact_stats(self) -> Dict[str, Any]:
        """Get contact statistics for dashboard."""
        try:
            # Basic counts
            total_contacts = self.db.query(Contact).count()
            new_contacts = self.db.query(Contact).filter(
                Contact.status == ContactStatus.NEW
            ).count()
            
            # Pending replies
            pending_replies = self.db.query(Contact).filter(
                and_(
                    Contact.status.in_([ContactStatus.NEW, ContactStatus.READ]),
                    Contact.is_spam == False,
                    Contact.requires_follow_up == True
                )
            ).count()
            
            # This month contacts
            current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            this_month_contacts = self.db.query(Contact).filter(
                Contact.created_at >= current_month_start
            ).count()
            
            # Average response time
            replied_contacts = self.db.query(Contact).filter(
                and_(
                    Contact.replied_at.isnot(None),
                    Contact.created_at.isnot(None)
                )
            ).all()
            
            if replied_contacts:
                response_times = [
                    (contact.replied_at - contact.created_at).total_seconds() / 3600
                    for contact in replied_contacts
                ]
                avg_response_time = sum(response_times) / len(response_times)
            else:
                avg_response_time = 0
            
            # Contact types breakdown
            contact_type_stats = self.db.query(
                Contact.contact_type,
                func.count(Contact.id).label('count')
            ).group_by(Contact.contact_type).all()
            
            contact_types_breakdown = [
                {"type": ct.value, "count": count}
                for ct, count in contact_type_stats
            ]
            
            # Monthly trends (last 12 months)
            monthly_trends = []
            for i in range(12):
                month_start = (datetime.now() - timedelta(days=30*i)).replace(day=1)
                month_end = (month_start + timedelta(days=32)).replace(day=1)
                
                count = self.db.query(Contact).filter(
                    and_(
                        Contact.created_at >= month_start,
                        Contact.created_at < month_end
                    )
                ).count()
                
                monthly_trends.append({
                    "month": month_start.strftime("%Y-%m"),
                    "count": count
                })
            
            # Top sources
            source_stats = self.db.query(
                Contact.source,
                func.count(Contact.id).label('count')
            ).filter(
                Contact.source.isnot(None)
            ).group_by(Contact.source).order_by(
                desc(func.count(Contact.id))
            ).limit(10).all()
            
            top_sources = [
                {"source": source or "Unknown", "count": count}
                for source, count in source_stats
            ]
            
            return {
                "total_contacts": total_contacts,
                "new_contacts": new_contacts,
                "pending_replies": pending_replies,
                "this_month_contacts": this_month_contacts,
                "avg_response_time_hours": round(avg_response_time, 1),
                "contact_types_breakdown": contact_types_breakdown,
                "monthly_trends": list(reversed(monthly_trends)),
                "top_sources": top_sources
            }
            
        except Exception as e:
            logger.error(f"Failed to get contact stats: {e}")
            return {}
    
    def search_contacts(self, search_term: str) -> List[Contact]:
        """Search contacts by name, email, subject, or message."""
        search_pattern = f"%{search_term.lower()}%"
        
        return self.db.query(Contact).filter(
            or_(
                func.lower(Contact.name).like(search_pattern),
                func.lower(Contact.email).like(search_pattern),
                func.lower(Contact.subject).like(search_pattern),
                func.lower(Contact.message).like(search_pattern),
                func.lower(Contact.company).like(search_pattern)
            )
        ).all()
    
    def get_pending_replies(self) -> List[Contact]:
        """Get contacts that need replies."""
        return self.db.query(Contact).filter(
            and_(
                Contact.status.in_([ContactStatus.NEW, ContactStatus.READ]),
                Contact.is_spam == False,
                Contact.requires_follow_up == True
            )
        ).order_by(Contact.created_at).all()
    
    def get_overdue_contacts(self) -> List[Contact]:
        """Get contacts with overdue responses."""
        # Contacts older than 24 hours (48 hours for non-urgent)
        urgent_cutoff = datetime.utcnow() - timedelta(hours=4)
        normal_cutoff = datetime.utcnow() - timedelta(hours=24)
        
        return self.db.query(Contact).filter(
            and_(
                Contact.status.in_([ContactStatus.NEW, ContactStatus.READ]),
                Contact.is_spam == False,
                Contact.requires_follow_up == True,
                or_(
                    and_(
                        Contact.priority == ContactPriority.URGENT,
                        Contact.created_at <= urgent_cutoff
                    ),
                    and_(
                        Contact.priority != ContactPriority.URGENT,
                        Contact.created_at <= normal_cutoff
                    )
                )
            )
        ).order_by(Contact.created_at).all()
    
    async def _validate_contact_creation(self, contact_data: ContactCreate):
        """Validate contact creation business rules."""
        # Check for duplicate recent submissions (same email within 1 hour)
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        recent_contact = self.db.query(Contact).filter(
            and_(
                Contact.email == contact_data.email.lower(),
                Contact.created_at >= one_hour_ago
            )
        ).first()
        
        if recent_contact:
            raise ValidationError("A contact inquiry from this email was already submitted recently")
    
    def _detect_spam(self, contact_data: ContactCreate) -> bool:
        """Detect potential spam based on content and patterns."""
        spam_indicators = 0
        
        # Check for spam keywords
        spam_keywords = [
            "lottery", "winner", "million", "inheritance", "viagra", "casino",
            "loan", "credit", "debt", "free money", "make money fast",
            "click here", "limited time", "act now", "guaranteed"
        ]
        
        message_lower = contact_data.message.lower()
        subject_lower = contact_data.subject.lower()
        
        for keyword in spam_keywords:
            if keyword in message_lower or keyword in subject_lower:
                spam_indicators += 2
        
        # Check for excessive links
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls_in_message = len(re.findall(url_pattern, contact_data.message))
        
        if urls_in_message > 2:
            spam_indicators += 3
        elif urls_in_message > 0:
            spam_indicators += 1
        
        # Check for excessive capitalization
        if len(contact_data.message) > 0:
            caps_ratio = sum(1 for c in contact_data.message if c.isupper()) / len(contact_data.message)
            if caps_ratio > 0.5:
                spam_indicators += 2
        
        # Check for suspicious patterns
        if any(char * 3 in contact_data.message for char in "!@#$%"):
            spam_indicators += 1
        
        # Check email domain patterns (basic)
        suspicious_domains = [
            "tempmail", "10minutemail", "guerrillamail", "mailinator"
        ]
        email_domain = contact_data.email.split("@")[1].lower()
        
        if any(domain in email_domain for domain in suspicious_domains):
            spam_indicators += 3
        
        # Return True if spam score is high
        return spam_indicators >= 4
    
    def _determine_priority(self, contact_data: ContactCreate) -> ContactPriority:
        """Determine contact priority based on type and content."""
        # High priority conditions
        high_priority_conditions = [
            contact_data.contact_type == ContactType.COMPLAINT,
            "urgent" in contact_data.subject.lower(),
            "asap" in contact_data.message.lower(),
            "immediately" in contact_data.message.lower(),
            contact_data.contact_type == ContactType.PARTNERSHIP and contact_data.company
        ]
        
        # Low priority conditions
        low_priority_conditions = [
            contact_data.contact_type == ContactType.FEEDBACK,
            contact_data.is_newsletter_signup
        ]
        
        if any(high_priority_conditions):
            return ContactPriority.URGENT
        elif any(low_priority_conditions):
            return ContactPriority.LOW
        else:
            return ContactPriority.NORMAL
    
    async def _send_contact_notifications(self, contact: Contact):
        """Send confirmation and admin notification emails."""
        try:
            # Prepare contact data for email templates
            contact_data = {
                "id": contact.id,
                "name": contact.name,
                "email": contact.email,
                "phone": contact.phone,
                "company": contact.company,
                "subject": contact.subject,
                "message": contact.message,
                "contact_type": contact.contact_type.value if contact.contact_type else "general",
                "source": contact.source,
                "created_at": contact.created_at
            }
            
            # Send confirmation email to client
            await email_service.send_contact_confirmation(contact_data)
            
            # Send notification email to admin
            await email_service.send_admin_notification("contact", contact_data)
            
        except Exception as e:
            logger.error(f"Failed to send contact notifications: {e}")
            # Don't raise exception here - contact is already created
    
    def _apply_filters(self, query, filters: ContactFilter):
        """Apply filters to contact query."""
        if filters.status:
            query = query.filter(Contact.status == filters.status)
        
        if filters.contact_type:
            query = query.filter(Contact.contact_type == filters.contact_type)
        
        if filters.priority:
            query = query.filter(Contact.priority == filters.priority)
        
        if filters.is_spam is not None:
            query = query.filter(Contact.is_spam == filters.is_spam)
        
        if filters.requires_follow_up is not None:
            query = query.filter(Contact.requires_follow_up == filters.requires_follow_up)
        
        if filters.date_from:
            query = query.filter(Contact.created_at >= filters.date_from)
        
        if filters.date_to:
            query = query.filter(Contact.created_at <= filters.date_to)
        
        if filters.source:
            query = query.filter(Contact.source.ilike(f"%{filters.source}%"))
        
        if filters.search:
            search_pattern = f"%{filters.search.lower()}%"
            query = query.filter(
                or_(
                    func.lower(Contact.name).like(search_pattern),
                    func.lower(Contact.email).like(search_pattern),
                    func.lower(Contact.subject).like(search_pattern),
                    func.lower(Contact.message).like(search_pattern),
                    func.lower(Contact.company).like(search_pattern)
                )
            )
        
        return query