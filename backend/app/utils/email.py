import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)

settings = get_settings()


def send_email(
    to_email: str,
    subject: str,
    body: str,
    html_body: str = None
) -> bool:
    """Send email notification"""
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.SENDER_EMAIL
        msg["To"] = to_email
        
        # Attach plain text version
        msg.attach(MIMEText(body, "plain"))
        
        # Attach HTML version if provided
        if html_body:
            msg.attach(MIMEText(html_body, "html"))
        
        # Send email
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"Email sent to {to_email}")
        return True
    
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False


def send_verification_email(email: str, verification_link: str) -> bool:
    """Send email verification email"""
    subject = "Verify Your Email - CricAuction"
    body = f"Please verify your email by clicking: {verification_link}"
    html_body = f"""
    <html>
        <body>
            <h2>Email Verification</h2>
            <p>Please verify your email by clicking the link below:</p>
            <a href="{verification_link}">Verify Email</a>
            <p>This link will expire in 24 hours.</p>
        </body>
    </html>
    """
    
    return send_email(email, subject, body, html_body)


def send_password_reset_email(email: str, reset_link: str) -> bool:
    """Send password reset email"""
    subject = "Reset Your Password - CricAuction"
    body = f"Click the link to reset your password: {reset_link}"
    html_body = f"""
    <html>
        <body>
            <h2>Password Reset</h2>
            <p>Click the link below to reset your password:</p>
            <a href="{reset_link}">Reset Password</a>
            <p>This link will expire in 1 hour.</p>
        </body>
    </html>
    """
    
    return send_email(email, subject, body, html_body)


def send_auction_notification(
    email: str,
    auction_title: str,
    player_name: str = None
) -> bool:
    """Send auction notification email"""
    subject = f"Auction Update - {auction_title}"
    body = f"There's an update on the {auction_title} auction"
    
    if player_name:
        html_body = f"""
        <html>
            <body>
                <h2>Auction Update</h2>
                <p>A new bid has been placed on {player_name} in the {auction_title} auction.</p>
                <p>Visit the app to see the latest bids.</p>
            </body>
        </html>
        """
    else:
        html_body = f"""
        <html>
            <body>
                <h2>Auction Update</h2>
                <p>There's an update on the {auction_title} auction.</p>
                <p>Visit the app for more details.</p>
            </body>
        </html>
        """
    
    return send_email(email, subject, body, html_body)
