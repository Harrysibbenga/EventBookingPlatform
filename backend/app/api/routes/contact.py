"""
API routes for contact form management.
Handles HTTP requests for general contact inquiries.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
import math

from app.core.database import get_db
from app.schemas.contact import (
    ContactCreate, ContactResponse, ContactUpdate, ContactList,
    ContactStats, ContactFilter, ContactConfirmation, ContactFormOptions,
    ContactReply
)
from app.services.contact_service import ContactService
from app.models.contact import ContactType, ContactStatus, ContactPriority
from app.utils.logger import get_logger
from app.utils.exceptions import ContactServiceError, ValidationError

logger = get_logger(__name__)
router = APIRouter(prefix="/contact")


@router.post("/", response_model=ContactConfirmation, status_code=201)
async def create_contact(
    contact_data: ContactCreate,
    db: Session = Depends(get_db)
):
    """
    Submit a new contact inquiry.
    
    This endpoint handles the submission of general contact forms from the website.
    It validates the data, creates the contact record, and sends confirmation emails.
    """
    try:
        service = ContactService(db)
        contact = await service.create_contact(contact_data)
        
        # Generate confirmation response
        reference_number = f"CT{contact.id:06d}"
        
        # Determine estimated response time based on inquiry type and priority
        response_time = "24 hours"
        if contact.contact_type == ContactType.GENERAL:
            response_time = "24-48 hours"
        elif contact.contact_type == ContactType.URGENT:
            response_time = "4-8 hours"
        
        return ContactConfirmation(
            success=True,
            contact_id=contact.id,
            message="Thank you for contacting us! We have received your message.",
            reference_number=reference_number,
            estimated_response_time=response_time
        )
        
    except ValidationError as e:
        logger.warning(f"Contact validation error: {e}")
        raise HTTPException(status_code=422, detail=str(e))
    
    except ContactServiceError as e:
        logger.error(f"Contact service error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process contact inquiry")
    
    except Exception as e:
        logger.error(f"Unexpected error creating contact: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=ContactList)
def get_contacts(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[ContactStatus] = Query(None, description="Filter by status"),
    contact_type: Optional[ContactType] = Query(None, description="Filter by contact type"),
    priority: Optional[ContactPriority] = Query(None, description="Filter by priority"),
    is_spam: Optional[bool] = Query(None, description="Filter spam messages"),
    search: Optional[str] = Query(None, min_length=3, description="Search term"),
    sort_by: str = Query("created_at", description="Sort field"),
    sort_order: str = Query("desc", regex="^(asc|desc)$", description="Sort order"),
    db: Session = Depends(get_db)
):
    """
    Get paginated list of contact inquiries.
    
    Admin endpoint for viewing and managing contact inquiries with filtering,
    searching, and sorting capabilities.
    """
    try:
        # Create filter object
        filters = ContactFilter(
            status=status,
            contact_type=contact_type,
            priority=priority,
            is_spam=is_spam,
            search=search
        )
        
        service = ContactService(db)
        contacts, total = service.get_contacts(
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
        
        return ContactList(
            contacts=[ContactResponse.from_orm(contact) for contact in contacts],
            total=total,
            page=page,
            per_page=per_page,
            pages=pages,
            has_next=has_next,
            has_prev=has_prev
        )
        
    except Exception as e:
        logger.error(f"Error fetching contacts: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch contacts")


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(
    contact_id: int = Path(..., ge=1, description="Contact ID"),
    db: Session = Depends(get_db)
):
    """
    Get a specific contact inquiry by ID.
    
    Admin endpoint for viewing detailed contact information.
    Automatically marks the contact as read when accessed.
    """
    try:
        service = ContactService(db)
        contact = service.get_contact(contact_id)
        
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        # Mark as read if it's new
        service.mark_as_read(contact_id)
        
        return ContactResponse.from_orm(contact)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching contact {contact_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch contact")


@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: int = Path(..., ge=1, description="Contact ID"),
    update_data: ContactUpdate = ...,
    db: Session = Depends(get_db)
):
    """
    Update a contact inquiry.
    
    Admin endpoint for updating contact status, priority, notes, and other fields.
    """
    try:
        service = ContactService(db)
        contact = service.update_contact(contact_id, update_data)
        
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        return ContactResponse.from_orm(contact)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating contact {contact_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update contact")


@router.delete("/{contact_id}")
def delete_contact(
    contact_id: int = Path(..., ge=1, description="Contact ID"),
    db: Session = Depends(get_db)
):
    """
    Delete a contact inquiry.
    
    Admin endpoint for permanently removing contact inquiries (typically spam).
    """
    try:
        service = ContactService(db)
        success = service.delete_contact(contact_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        return {"message": "Contact deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting contact {contact_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete contact")


@router.post("/{contact_id}/reply")
async def reply_to_contact(
    contact_id: int = Path(..., ge=1, description="Contact ID"),
    reply_data: ContactReply = ...,
    db: Session = Depends(get_db)
):
    """
    Send a reply to a contact inquiry.
    
    Admin endpoint for responding to contact inquiries via email.
    """
    try:
        service = ContactService(db)
        success = await service.reply_to_contact(contact_id, reply_data)
        
        if not success:
            raise HTTPException(status_code=404, detail="Contact not found or reply failed")
        
        return {"message": "Reply sent successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error replying to contact {contact_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to send reply")


@router.put("/{contact_id}/spam")
def mark_as_spam(
    contact_id: int = Path(..., ge=1, description="Contact ID"),
    is_spam: bool = Query(True, description="Mark as spam"),
    db: Session = Depends(get_db)
):
    """
    Mark or unmark a contact as spam.
    
    Admin endpoint for spam management.
    """
    try:
        service = ContactService(db)
        contact = service.mark_as_spam(contact_id, is_spam)
        
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        
        action = "marked as spam" if is_spam else "unmarked as spam"
        return {"message": f"Contact {action} successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error marking contact {contact_id} as spam: {e}")
        raise HTTPException(status_code=500, detail="Failed to update spam status")


@router.get("/stats/dashboard", response_model=ContactStats)
def get_contact_stats(db: Session = Depends(get_db)):
    """
    Get contact statistics for admin dashboard.
    
    Returns aggregated statistics including counts, response times, and trends.
    """
    try:
        service = ContactService(db)
        stats = service.get_contact_stats()
        
        return ContactStats(**stats)
        
    except Exception as e:
        logger.error(f"Error fetching contact stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch statistics")


@router.get("/pending/replies")
def get_pending_replies(db: Session = Depends(get_db)):
    """
    Get contacts that need replies.
    
    Admin endpoint for identifying contacts that haven't been replied to
    and need attention.
    """
    try:
        service = ContactService(db)
        contacts = service.get_pending_replies()
        
        return [ContactResponse.from_orm(contact) for contact in contacts]
        
    except Exception as e:
        logger.error(f"Error fetching pending replies: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch pending replies")


@router.get("/overdue/responses")
def get_overdue_contacts(db: Session = Depends(get_db)):
    """
    Get contacts with overdue responses.
    
    Admin endpoint for identifying contacts that have exceeded the
    expected response time.
    """
    try:
        service = ContactService(db)
        contacts = service.get_overdue_contacts()
        
        return [ContactResponse.from_orm(contact) for contact in contacts]
        
    except Exception as e:
        logger.error(f"Error fetching overdue contacts: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch overdue contacts")


@router.get("/search/inquiries")
def search_contacts(
    q: str = Query(..., min_length=3, description="Search query"),
    db: Session = Depends(get_db)
):
    """
    Search contact inquiries.
    
    Admin endpoint for searching contacts by name, email, subject, or message content.
    """
    try:
        service = ContactService(db)
        contacts = service.search_contacts(q)
        
        return [ContactResponse.from_orm(contact) for contact in contacts]
        
    except Exception as e:
        logger.error(f"Error searching contacts: {e}")
        raise HTTPException(status_code=500, detail="Failed to search contacts")


@router.get("/form/options", response_model=ContactFormOptions)
def get_contact_form_options():
    """
    Get configuration options for the contact form.
    
    Public endpoint that provides form options like contact types,
    sources, and other configuration data for the frontend.
    """
    try:
        # Contact type options
        contact_types = [
            {"value": ContactType.GENERAL.value, "label": "General Inquiry", "description": "General questions and information"},
            {"value": ContactType.PRICING.value, "label": "Pricing Information", "description": "Questions about pricing and packages"},
            {"value": ContactType.AVAILABILITY.value, "label": "Availability Check", "description": "Check availability for specific dates"},
            {"value": ContactType.SERVICES.value, "label": "Services Information", "description": "Questions about our services"},
            {"value": ContactType.PARTNERSHIP.value, "label": "Partnership Opportunity", "description": "Business partnership inquiries"},
            {"value": ContactType.FEEDBACK.value, "label": "Feedback", "description": "Customer feedback and testimonials"},
            {"value": ContactType.COMPLAINT.value, "label": "Complaint", "description": "Service complaints or issues"},
            {"value": ContactType.OTHER.value, "label": "Other", "description": "Other inquiries not listed above"}
        ]
        
        # Source options (how they heard about us)
        sources = [
            "Google Search",
            "Social Media (Facebook)",
            "Social Media (Instagram)",
            "Social Media (Twitter)",
            "Social Media (LinkedIn)",
            "Word of Mouth",
            "Referral from Friend",
            "Wedding Website/Blog",
            "Event Planning Website",
            "Advertisement",
            "Previous Client",
            "Other"
        ]
        
        # Timezone options (major US timezones)
        timezones = [
            {"value": "America/New_York", "label": "Eastern Time (ET)"},
            {"value": "America/Chicago", "label": "Central Time (CT)"},
            {"value": "America/Denver", "label": "Mountain Time (MT)"},
            {"value": "America/Los_Angeles", "label": "Pacific Time (PT)"},
            {"value": "America/Anchorage", "label": "Alaska Time (AKT)"},
            {"value": "Pacific/Honolulu", "label": "Hawaii Time (HT)"}
        ]
        
        # Preferred contact times
        preferred_times = [
            "Morning (9 AM - 12 PM)",
            "Afternoon (12 PM - 5 PM)",
            "Evening (5 PM - 8 PM)",
            "Weekdays Only",
            "Weekends Only",
            "Anytime"
        ]
        
        return ContactFormOptions(
            contact_types=contact_types,
            sources=sources,
            timezones=timezones,
            preferred_times=preferred_times,
            max_message_length=2000
        )
        
    except Exception as e:
        logger.error(f"Error fetching contact form options: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch form options")