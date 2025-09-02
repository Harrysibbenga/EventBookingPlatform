"""
Email service for sending notifications and communications.
Handles SMTP configuration, email templates, and delivery tracking.
Enhanced version with robust connection handling and retry logic.
"""

from __future__ import annotations

import os
import logging
from typing import Optional, List, Dict, Any
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import asyncio
import aiosmtplib
from datetime import datetime, date

from app.core.config import get_settings
from app.utils.logger import get_logger
from app.utils.exceptions import EmailServiceError

logger = get_logger(__name__)
settings = get_settings()


def _to_bool(v: Any, default: bool = False) -> bool:
    """Convert various input types to boolean."""
    if isinstance(v, bool):
        return v
    if v is None:
        return default
    return str(v).strip().lower() in {"1", "true", "t", "yes", "y", "on"}


def _to_int(v: Any, default: int) -> int:
    """Convert various input types to integer with fallback."""
    try:
        return int(v)
    except Exception:
        return default


class EmailTemplate:
    """Email template management with business-specific templates."""
    
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
        <li><strong>Priority:</strong> {priority_text}</li>
    </ul>
    
    <p><strong>Action Required:</strong> Please respond within 24 hours.</p>
    
    <hr>
    <p><small>Booking ID: {booking_id} | Submitted: {created_at}</small></p>
    """


class EmailService:
    """
    Async Gmail SMTP email sender with robust connection handling.
    
    Features:
    - Supports port 587 (STARTTLS) and 465 (implicit SSL)
    - Handles CC/BCC, attachments, and retries
    - Railway-safe environment variable parsing
    - Business email templates for booking and contact confirmations
    """

    def __init__(self) -> None:
        # Accept both naming schemes; prefer USER/PASS if present
        self.smtp_host: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port: int = _to_int(os.getenv("SMTP_PORT", 587), 587)

        self.smtp_username: str = (
            os.getenv("SMTP_USER")
            or os.getenv("SMTP_USERNAME") 
            or settings.SMTP_USERNAME
            or ""
        )
        self.smtp_password: str = (
            os.getenv("SMTP_PASS")
            or os.getenv("SMTP_PASSWORD")
            or settings.SMTP_PASSWORD
            or ""
        )

        self.from_email: str = (
            os.getenv("SMTP_FROM_EMAIL") 
            or settings.SMTP_FROM_EMAIL 
            or self.smtp_username
        )
        self.from_name: str = (
            os.getenv("SMTP_FROM_NAME") 
            or settings.SMTP_FROM_NAME 
            or ""
        )
        self.use_tls: bool = _to_bool(
            os.getenv("SMTP_USE_TLS") or getattr(settings, 'SMTP_USE_TLS', True), 
            True
        )

        self.default_timeout: int = _to_int(os.getenv("SMTP_TIMEOUT", 20), 20)
        self.max_retries: int = _to_int(os.getenv("SMTP_MAX_RETRIES", 2), 2)
        self.retry_backoff_base: float = float(os.getenv("SMTP_BACKOFF_BASE", "1.5"))

        logger.info(
            "SMTP config host=%s port=%s tls=%s user=%s",
            self.smtp_host, self.smtp_port, self.use_tls, self.smtp_username
        )

    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        attachments: Optional[List[Dict[str, Any]]] = None,
    ) -> bool:
        """
        Send an email (HTML + optional plain text), with CC/BCC/attachments.
        Returns True on success, False on failure.
        """
        msg = self._build_message(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
            text_content=text_content,
            cc=cc,
            attachments=attachments,
        )

        recipients = [to_email] + (cc or []) + (bcc or [])
        try:
            await self._send_smtp_with_retry(msg, recipients)
            logger.info("Email sent to %s", to_email)
            return True
        except Exception as e:
            logger.error("Failed to send email to %s: %s", to_email, e, exc_info=True)
            return False

    async def send_booking_confirmation(self, booking_data: Dict[str, Any]) -> bool:
        """Send booking confirmation email to client."""
        try:
            # Format budget range
            budget_range = "Not specified"
            if booking_data.get("budget_min") and booking_data.get("budget_max"):
                budget_range = f"${booking_data['budget_min']:,.2f} - ${booking_data['budget_max']:,.2f}"
            elif booking_data.get("budget_min"):
                budget_range = f"${booking_data['budget_min']:,.2f}+"
            elif booking_data.get("budget_max"):
                budget_range = f"Up to ${booking_data['budget_max']:,.2f}"
            
            # Generate reference number
            reference_number = f"BK{booking_data['id']:06d}"
            
            # Prepare template data
            template_data = {
                "contact_name": booking_data["contact_name"],
                "event_type": booking_data.get("event_type", "").replace("_", " ").title(),
                "event_date": self._format_date_for_display(booking_data.get("event_date")),
                "guest_count": booking_data.get("guest_count", "Not specified"),
                "venue_name": booking_data.get("venue_name", "To be determined"),
                "budget_range": budget_range,
                "preferred_contact": booking_data.get("preferred_contact", "email").replace("_", " ").title(),
                "business_email": getattr(settings, 'BUSINESS_EMAIL', 'info@business.com'),
                "business_phone": getattr(settings, 'BUSINESS_PHONE', 'Please see our website'),
                "business_name": getattr(settings, 'BUSINESS_NAME', 'Event Services'),
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
                "business_phone": getattr(settings, 'BUSINESS_PHONE', 'Please see our website'),
                "business_name": getattr(settings, 'BUSINESS_NAME', 'Event Services'),
                "reference_number": reference_number
            }
            
            # Format HTML content
            html_content = EmailTemplate.CONTACT_CONFIRMATION.format(**template_data)
            
            # Send email
            return await self.send_email(
                to_email=contact_data["email"],
                subject=f"Thank you for contacting {template_data['business_name']}",
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
            admin_email = getattr(settings, 'ADMIN_EMAIL', None) or getattr(settings, 'BUSINESS_EMAIL', 'admin@business.com')
            
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

    async def test_connection(self) -> bool:
        """
        Test SMTP connection with proper SSL/TLS handling.
        """
        try:
            smtp, starttls = self._build_client()
            await smtp.connect()
            if starttls:
                await smtp.starttls()
            if self.smtp_username and self.smtp_password:
                await smtp.login(self.smtp_username, self.smtp_password)
            await smtp.quit()
            logger.info("SMTP connection OK")
            return True
        except Exception as e:
            logger.error("SMTP connection failed: %s", e, exc_info=True)
            return False

    # ---------------------- Internal Methods ----------------------

    def _build_message(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str],
        cc: Optional[List[str]],
        attachments: Optional[List[Dict[str, Any]]],
    ) -> MIMEMultipart:
        """Build complete email message with proper MIME structure."""
        msg = MIMEMultipart("mixed")

        # Headers
        frm = f"{self.from_name} <{self.from_email}>" if self.from_name else self.from_email
        msg["From"] = frm
        msg["To"] = to_email
        if cc:
            msg["Cc"] = ", ".join(cc)
        msg["Subject"] = subject

        # Body: alternative (plain + html)
        alt = MIMEMultipart("alternative")
        if text_content:
            alt.attach(MIMEText(text_content, "plain", "utf-8"))
        alt.attach(MIMEText(html_content, "html", "utf-8"))
        msg.attach(alt)

        # Attachments
        if attachments:
            for a in attachments:
                self._add_attachment(msg, a)

        return msg

    def _add_attachment(self, message: MIMEMultipart, attachment: Dict[str, Any]) -> None:
        """
        Add attachment to message.
        attachment dict: {"path": "/path/file.pdf", "filename": "file.pdf", "mime": "application/pdf"}
        """
        try:
            path = Path(attachment["path"])
            data = path.read_bytes()
            mime = (attachment.get("mime") or "application/octet-stream").split("/", 1)
            maintype, subtype = mime[0], (mime[1] if len(mime) > 1 else "octet-stream")

            part = MIMEBase(maintype, subtype)
            part.set_payload(data)
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f'attachment; filename="{attachment.get("filename", path.name)}"',
            )
            message.attach(part)
        except Exception as e:
            logger.error(
                "Failed to add attachment %s: %s",
                attachment.get("filename") or attachment.get("path"),
                e,
            )

    def _build_client(self) -> tuple[aiosmtplib.SMTP, bool]:
        """
        Build SMTP client with proper SSL/TLS configuration.
        Returns (client, starttls_flag)
        """
        if self.smtp_port == 465:
            # Implicit SSL
            client = aiosmtplib.SMTP(
                hostname=self.smtp_host,
                port=self.smtp_port,
                use_tls=True,
                timeout=self.default_timeout,
            )
            return client, False
        else:
            # Plain connection, possibly with STARTTLS
            client = aiosmtplib.SMTP(
                hostname=self.smtp_host,
                port=self.smtp_port,
                timeout=self.default_timeout,
            )
            return client, self.use_tls and self.smtp_port == 587

    async def _send_smtp_with_retry(self, message: MIMEMultipart, recipients: List[str]) -> None:
        """
        Send message with exponential backoff retry logic.
        Raises the last exception if all retries fail.
        """
        attempt = 0
        last_exc: Optional[Exception] = None

        while attempt <= self.max_retries:
            try:
                smtp, starttls = self._build_client()
                await smtp.connect()
                
                if starttls:
                    await smtp.starttls()

                if self.smtp_username and self.smtp_password:
                    await smtp.login(self.smtp_username, self.smtp_password)

                resp = await smtp.send_message(message, recipients=recipients)
                logger.debug("SMTP send response: %s", resp)

                await smtp.quit()
                return
                
            except Exception as e:
                last_exc = e
                if attempt < self.max_retries:
                    delay = (self.retry_backoff_base ** attempt)
                    logger.warning(
                        "SMTP send attempt %s failed: %s (retrying in %.1fs)",
                        attempt + 1, e, delay
                    )
                    await asyncio.sleep(delay)
                attempt += 1

        # Out of retries
        raise last_exc if last_exc else RuntimeError("Unknown SMTP send error")

    async def _send_booking_admin_notification(
        self,
        admin_email: str,
        booking_data: Dict[str, Any]
    ) -> bool:
        """Send booking notification to admin with urgency detection."""
        try:
            # Check if this is urgent based on event date
            is_urgent = False
            if booking_data.get("event_date"):
                event_date = booking_data["event_date"]
                if isinstance(event_date, datetime):
                    days_until_event = (event_date.date() - date.today()).days
                elif isinstance(event_date, date):
                    days_until_event = (event_date - date.today()).days
                else:
                    days_until_event = 365  # Default to non-urgent
                is_urgent = days_until_event <= 30
            
            # Format all template data
            template_data = {
                "booking_id": booking_data["id"],
                "contact_name": booking_data["contact_name"],
                "contact_email": booking_data["contact_email"],
                "contact_phone": booking_data.get("contact_phone", "Not provided"),
                "preferred_contact": booking_data.get("preferred_contact", "email").replace("_", " ").title(),
                "event_type": booking_data.get("event_type", "unknown").replace("_", " ").title(),
                "event_date": self._format_date_for_display(booking_data.get("event_date")),
                "event_time": self._format_time_for_display(booking_data.get("event_time")),
                "duration_hours": booking_data.get("duration_hours", "Not specified"),
                "guest_count": booking_data.get("guest_count", "Not specified"),
                "venue_name": booking_data.get("venue_name", "Not specified"),
                "venue_address": booking_data.get("venue_address", "Not specified"),
                "budget_range": self._format_budget_range(booking_data),
                "services_needed": booking_data.get("services_needed", "Not specified"),
                "special_requirements": booking_data.get("special_requirements", "None"),
                "how_heard_about_us": booking_data.get("how_heard_about_us", "Not specified"),
                "previous_client": "Yes" if booking_data.get("previous_client") else "No",
                "priority_text": "HIGH" if is_urgent else "Normal",
                "created_at": self._safe_datetime_format(booking_data.get("created_at"))
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
                <li><strong>Type:</strong> {contact_data.get('contact_type', 'general').replace('_', ' ').title()}</li>
                <li><strong>Source:</strong> {contact_data.get('source', 'Not specified')}</li>
            </ul>
            
            <h3>Message:</h3>
            <blockquote style="border-left: 3px solid #ccc; padding-left: 15px; margin: 15px 0;">
                {contact_data['message']}
            </blockquote>
            
            <hr>
            <p><small>Contact ID: {contact_data['id']} | Submitted: {self._safe_datetime_format(contact_data.get('created_at'))}</small></p>
            """
            
            return await self.send_email(
                to_email=admin_email,
                subject=subject,
                html_content=html_content
            )
            
        except Exception as e:
            logger.error(f"Failed to send contact admin notification: {e}")
            return False

    def _format_date_for_display(self, date_value) -> str:
        """Format date for email display."""
        if not date_value:
            return "Not specified"
        if isinstance(date_value, datetime):
            return date_value.strftime("%B %d, %Y")
        elif isinstance(date_value, date):
            return date_value.strftime("%B %d, %Y")
        return str(date_value)

    def _format_time_for_display(self, time_value) -> str:
        """Format time for email display."""
        if not time_value:
            return "Not specified"
        if isinstance(time_value, str):
            return time_value
        return time_value.strftime("%I:%M %p")

    def _format_budget_range(self, booking_data: Dict[str, Any]) -> str:
        """Format budget range for display."""
        if booking_data.get("budget_min") and booking_data.get("budget_max"):
            return f"${booking_data['budget_min']:,.2f} - ${booking_data['budget_max']:,.2f}"
        elif booking_data.get("budget_min"):
            return f"${booking_data['budget_min']:,.2f}+"
        elif booking_data.get("budget_max"):
            return f"Up to ${booking_data['budget_max']:,.2f}"
        return "Not specified"

    def _safe_datetime_format(self, dt_value) -> str:
        """Safely format datetime/date values for email templates."""
        if not dt_value:
            return datetime.now().strftime("%B %d, %Y at %I:%M %p")
        
        if isinstance(dt_value, datetime):
            return dt_value.strftime("%B %d, %Y at %I:%M %p")
        elif isinstance(dt_value, date):
            dt = datetime.combine(dt_value, datetime.min.time())
            return dt.strftime("%B %d, %Y at %I:%M %p")
        else:
            return str(dt_value)


# Global email service instance
email_service = EmailService()