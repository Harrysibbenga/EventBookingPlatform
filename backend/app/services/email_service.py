"""
Email service for sending notifications and communications.
Handles SMTP configuration, email templates, and delivery tracking.
"""

import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional, Dict, Any
from pathlib import Path
import asyncio
from datetime import datetime
import json

from app.core.config import get_settings
from app.utils.logger import get_logger
from app.utils.exceptions import EmailServiceError

logger = get_logger(__name__)
settings = get_settings()


class EmailTemplate:
    """Email template management."""
    
    BOOKING_CONFIRMATION = """
    <h2>Thank you for your booking inquiry!</h2>
    
    <p>Dear {contact_name},</p>
    
    <p>Thank you for your interest in our event services. We have received your booking inquiry for a <strong>{event_type}</strong> on <strong>{event_date}</strong>.</p>
    
    <h3>Your Inquiry Details:</h3>
    <ul>
        <li><strong>Event Type:</strong> {event_type}</li>
        <li><strong>Event Date:</strong> {event_date}</li>
        <li><strong>Guest Count:</strong> {guest_count}</li>
        <li><strong>Venue:</strong> {venue_name}</li>
        <li><strong>Budget Range:</strong> {budget_range}</li>
    </ul>
    
    <h3>Next Steps:</h3>
    <ol>
        <li>We will review your inquiry within 24 hours</li>
        <li>A member of our team will contact you via {preferred_contact}</li>
        <li>We'll discuss your requirements and provide a detailed quote</li>
        <li>Once approved, we'll send you a contract to secure your date</li>
    </ol>
    
    <p>If you have any immediate questions, please don't hesitate to contact us at {business_email} or {business_phone}.</p>
    
    <p>We look forward to making your event memorable!</p>
    
    <p>Best regards,<br>
    {business_name} Team</p>
    
    <hr>
    <p><small>Reference Number: {reference_number}</small></p>
    """
    
    CONTACT_CONFIRMATION = """
    <h2>Thank you for contacting us!</h2>
    
    <p>Dear {name},</p>
    
    <p>Thank you for reaching out to us. We have received your message regarding <strong>{subject}</strong>.</p>
    
    <h3>Your Message:</h3>
    <blockquote style="border-left: 3px solid #ccc; padding-left: 15px; margin: 15px 0;">
        {message}
    </blockquote>
    
    <p>We typically respond to inquiries within 24 hours during business days. If your inquiry is urgent, please call us at {business_phone}.</p>
    
    <p>Best regards,<br>
    {business_name} Team</p>
    
    <hr>
    <p><small>Reference Number: {reference_number}</small></p>
    """
    
    BOOKING_ADMIN_NOTIFICATION = """
    <h2>New Booking Inquiry Received</h2>
    
    <p>A new booking inquiry has been submitted:</p>
    
    <h3>Contact Information:</h3>
    <ul>
        <li><strong>Name:</strong> {contact_name}</li>
        <li><strong>Email:</strong> {contact_email}</li>
        <li><strong>Phone:</strong> {contact_phone}</li>
        <li><strong>Preferred Contact:</strong> {preferred_contact}</li>
    </ul>
    
    <h3>Event Details:</h3>
    <ul>
        <li><strong>Event Type:</strong> {event_type}</li>
        <li><strong>Event Date:</strong> {event_date}</li>
        <li><strong>Event Time:</strong> {event_time}</li>
        <li><strong>Duration:</strong> {duration_hours} hours</li>
        <li><strong>Guest Count:</strong> {guest_count}</li>
        <li><strong>Venue:</strong> {venue_name} ({venue_address})</li>
    </ul>
    
    <h3>Budget & Services:</h3>
    <ul>
        <li><strong>Budget Range:</strong> {budget_range}</li>
        <li><strong>Services Needed:</strong> {services_needed}</li>
        <li><strong>Special Requirements:</strong> {special_requirements}</li>
    </ul>
    
    <h3>Additional Information:</h3>
    <ul>
        <li><strong>How they heard about us:</strong> {how_heard_about_us}</li>
        <li><strong>Previous client:</strong> {previous_client}</li>
        <li><strong>Priority:</strong> {"HIGH" if is_urgent else "Normal"}</li>
    </ul>
    
    <p><strong>Action Required:</strong> Please respond within 24 hours.</p>
    
    <hr>
    <p><small>Booking ID: {booking_id} | Submitted: {created_at}</small></p>
    """


class EmailService:
    """Email service for sending notifications and communications."""
    
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_FROM_EMAIL
        self.from_name = settings.SMTP_FROM_NAME
        self.use_tls = settings.SMTP_USE_TLS
        
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        attachments: Optional[List[Dict[str, Any]]] = None
    ) -> bool:
        """
        Send an email using SMTP.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML email content
            text_content: Plain text content (optional)
            cc: CC recipients (optional)
            bcc: BCC recipients (optional)
            attachments: List of attachments (optional)
            
        Returns:
            bool: True if email sent successfully
        """
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["From"] = f"{self.from_name} <{self.from_email}>"
            message["To"] = to_email
            message["Subject"] = subject
            
            if cc:
                message["Cc"] = ", ".join(cc)
            
            # Add text content
            if text_content:
                text_part = MIMEText(text_content, "plain")
                message.attach(text_part)
            
            # Add HTML content
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Add attachments
            if attachments:
                for attachment in attachments:
                    self._add_attachment(message, attachment)
            
            # Send email
            await self._send_smtp(message, to_email, cc, bcc)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            raise EmailServiceError(f"Failed to send email: {e}")
    
    async def _send_smtp(
        self,
        message: MIMEMultipart,
        to_email: str,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ):
        """Send email via SMTP."""
        recipients = [to_email]
        if cc:
            recipients.extend(cc)
        if bcc:
            recipients.extend(bcc)
        
        smtp = aiosmtplib.SMTP(hostname=self.smtp_host, port=self.smtp_port)
        
        try:
            await smtp.connect()
            if self.use_tls:
                await smtp.starttls()
            await smtp.login(self.smtp_username, self.smtp_password)
            await smtp.send_message(message, recipients=recipients)
        finally:
            await smtp.quit()
    
    def _add_attachment(self, message: MIMEMultipart, attachment: Dict[str, Any]):
        """Add attachment to email message."""
        try:
            with open(attachment["path"], "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {attachment['filename']}"
            )
            message.attach(part)
            
        except Exception as e:
            logger.error(f"Failed to add attachment {attachment['filename']}: {e}")
    
    async def send_booking_confirmation(self, booking_data: Dict[str, Any]) -> bool:
        """Send booking confirmation email to client."""
        try:
            # Format budget range
            budget_range = "Not specified"
            if booking_data.get("budget_min") and booking_data.get("budget_max"):
                budget_range = f"${booking_data['budget_min']:,.2f} - ${booking_data['budget_max']:,.2f}"
            elif booking_data.get("budget_min"):
                budget_range = f"${booking_data['budget_min']:,.2f}+"
            
            # Generate reference number
            reference_number = f"BK{booking_data['id']:06d}"
            
            # Prepare template data
            template_data = {
                "contact_name": booking_data["contact_name"],
                "event_type": booking_data["event_type"].replace("_", " ").title(),
                "event_date": booking_data["event_date"].strftime("%B %d, %Y"),
                "guest_count": booking_data["guest_count"],
                "venue_name": booking_data.get("venue_name", "To be determined"),
                "budget_range": budget_range,
                "preferred_contact": booking_data["preferred_contact"].replace("_", " ").title(),
                "business_email": settings.BUSINESS_EMAIL,
                "business_phone": settings.BUSINESS_PHONE or "Please see our website",
                "business_name": settings.BUSINESS_NAME,
                "reference_number": reference_number
            }
            
            # Format HTML content
            html_content = EmailTemplate.BOOKING_CONFIRMATION.format(**template_data)
            
            # Send email
            return await self.send_email(
                to_email=booking_data["contact_email"],
                subject=f"Booking Inquiry Confirmation - {template_data['event_type']}",
                html_content=html_content
            )
            
        except Exception as e:
            logger.error(f"Failed to send booking confirmation: {e}")
            return False
    
    async def send_contact_confirmation(self, contact_data: Dict[str, Any]) -> bool:
        """Send contact form confirmation email."""
        try:
            # Generate reference number
            reference_number = f"CT{contact_data['id']:06d}"
            
            # Prepare template data
            template_data = {
                "name": contact_data["name"],
                "subject": contact_data["subject"],
                "message": contact_data["message"],
                "business_phone": settings.BUSINESS_PHONE or "Please see our website",
                "business_name": settings.BUSINESS_NAME,
                "reference_number": reference_number
            }
            
            # Format HTML content
            html_content = EmailTemplate.CONTACT_CONFIRMATION.format(**template_data)
            
            # Send email
            return await self.send_email(
                to_email=contact_data["email"],
                subject=f"Thank you for contacting {settings.BUSINESS_NAME}",
                html_content=html_content
            )
            
        except Exception as e:
            logger.error(f"Failed to send contact confirmation: {e}")
            return False
    
    async def send_admin_notification(
        self,
        notification_type: str,
        data: Dict[str, Any]
    ) -> bool:
        """Send notification email to admin."""
        try:
            admin_email = settings.ADMIN_EMAIL or settings.BUSINESS_EMAIL
            
            if notification_type == "booking":
                return await self._send_booking_admin_notification(admin_email, data)
            elif notification_type == "contact":
                return await self._send_contact_admin_notification(admin_email, data)
            else:
                logger.error(f"Unknown notification type: {notification_type}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send admin notification: {e}")
            return False
    
    async def _send_booking_admin_notification(
        self,
        admin_email: str,
        booking_data: Dict[str, Any]
    ) -> bool:
        """Send booking notification to admin."""
        try:
            # Check if urgent (event within 30 days)
            event_date = booking_data.get("event_date")
            is_urgent = False
            if event_date:
                days_until_event = (event_date - datetime.now().date()).days
                is_urgent = days_until_event <= 30
            
            # Format budget range
            budget_range = "Not specified"
            if booking_data.get("budget_min") and booking_data.get("budget_max"):
                budget_range = f"${booking_data['budget_min']:,.2f} - ${booking_data['budget_max']:,.2f}"
            elif booking_data.get("budget_min"):
                budget_range = f"${booking_data['budget_min']:,.2f}+"
            
            # Prepare template data
            template_data = {
                "booking_id": booking_data["id"],
                "contact_name": booking_data["contact_name"],
                "contact_email": booking_data["contact_email"],
                "contact_phone": booking_data.get("contact_phone", "Not provided"),
                "preferred_contact": booking_data["preferred_contact"].replace("_", " ").title(),
                "event_type": booking_data["event_type"].replace("_", " ").title(),
                "event_date": booking_data["event_date"].strftime("%B %d, %Y"),
                "event_time": booking_data.get("event_time", "Not specified"),
                "duration_hours": booking_data.get("duration_hours", "Not specified"),
                "guest_count": booking_data["guest_count"],
                "venue_name": booking_data.get("venue_name", "Not specified"),
                "venue_address": booking_data.get("venue_address", "Not specified"),
                "budget_range": budget_range,
                "services_needed": booking_data.get("services_needed", "Not specified"),
                "special_requirements": booking_data.get("special_requirements", "None"),
                "how_heard_about_us": booking_data.get("how_heard_about_us", "Not specified"),
                "previous_client": "Yes" if booking_data.get("previous_client") else "No",
                "is_urgent": is_urgent,
                "created_at": booking_data.get("created_at", datetime.now()).strftime("%B %d, %Y at %I:%M %p")
            }
            
            # Format HTML content
            html_content = EmailTemplate.BOOKING_ADMIN_NOTIFICATION.format(**template_data)
            
            # Set subject with urgency indicator
            subject = f"{'🔥 URGENT - ' if is_urgent else ''}New Booking Inquiry: {template_data['event_type']}"
            
            # Send email
            return await self.send_email(
                to_email=admin_email,
                subject=subject,
                html_content=html_content
            )
            
        except Exception as e:
            logger.error(f"Failed to send booking admin notification: {e}")
            return False
    
    async def _send_contact_admin_notification(
        self,
        admin_email: str,
        contact_data: Dict[str, Any]
    ) -> bool:
        """Send contact form notification to admin."""
        try:
            subject = f"New Contact Inquiry: {contact_data['subject']}"
            
            html_content = f"""
            <h2>New Contact Inquiry Received</h2>
            
            <h3>Contact Information:</h3>
            <ul>
                <li><strong>Name:</strong> {contact_data['name']}</li>
                <li><strong>Email:</strong> {contact_data['email']}</li>
                <li><strong>Phone:</strong> {contact_data.get('phone', 'Not provided')}</li>
                <li><strong>Company:</strong> {contact_data.get('company', 'Not provided')}</li>
            </ul>
            
            <h3>Inquiry Details:</h3>
            <ul>
                <li><strong>Subject:</strong> {contact_data['subject']}</li>
                <li><strong>Type:</strong> {contact_data['contact_type'].replace('_', ' ').title()}</li>
                <li><strong>Source:</strong> {contact_data.get('source', 'Not specified')}</li>
            </ul>
            
            <h3>Message:</h3>
            <blockquote style="border-left: 3px solid #ccc; padding-left: 15px; margin: 15px 0;">
                {contact_data['message']}
            </blockquote>
            
            <hr>
            <p><small>Contact ID: {contact_data['id']} | Submitted: {contact_data.get('created_at', datetime.now()).strftime('%B %d, %Y at %I:%M %p')}</small></p>
            """
            
            return await self.send_email(
                to_email=admin_email,
                subject=subject,
                html_content=html_content
            )
            
        except Exception as e:
            logger.error(f"Failed to send contact admin notification: {e}")
            return False
    
    async def test_connection(self) -> bool:
        """Test SMTP connection."""
        try:
            smtp = aiosmtplib.SMTP(hostname=self.smtp_host, port=self.smtp_port)
            await smtp.connect()
            if self.use_tls:
                await smtp.starttls()
            await smtp.login(self.smtp_username, self.smtp_password)
            await smtp.quit()
            logger.info("SMTP connection test successful")
            return True
        except Exception as e:
            logger.error(f"SMTP connection test failed: {e}")
            return False


# Global email service instance
email_service = EmailService()