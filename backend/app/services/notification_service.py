from typing import Optional, List
from sqlmodel import Session
from app.models.models import Notification
from app.repositories.notification_repository import NotificationRepository
from app.core.constants import NotificationEvent, NotificationType
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import get_settings


class NotificationService:
    """Notification service"""
    
    def __init__(self, session: Session):
        self.session = session
        self.notification_repo = NotificationRepository(session)
        self.settings = get_settings()
    
    def send_email_notification(
        self,
        user_email: str,
        subject: str,
        message: str
    ) -> bool:
        """Send email notification"""
        try:
            with smtplib.SMTP(self.settings.SMTP_HOST, self.settings.SMTP_PORT) as server:
                server.starttls()
                server.login(self.settings.SMTP_USER, self.settings.SMTP_PASSWORD)
                
                msg = MIMEMultipart()
                msg["From"] = self.settings.SENDER_EMAIL
                msg["To"] = user_email
                msg["Subject"] = subject
                
                msg.attach(MIMEText(message, "html"))
                
                server.send_message(msg)
            
            return True
        
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False
    
    def create_in_app_notification(
        self,
        user_id: int,
        event: str,
        title: str,
        message: str
    ) -> Notification:
        """Create in-app notification"""
        notification = Notification(
            user_id=user_id,
            notification_type=NotificationType.IN_APP,
            event=event,
            title=title,
            message=message,
            is_read=False
        )
        
        return self.notification_repo.create_notification(notification)
    
    def notify_auction_started(
        self,
        user_id: int,
        user_email: str,
        auction_title: str
    ) -> None:
        """Send auction started notification"""
        # Create in-app notification
        self.create_in_app_notification(
            user_id=user_id,
            event=NotificationEvent.AUCTION_STARTED,
            title="Auction Started",
            message=f"The auction '{auction_title}' has started!"
        )
        
        # Send email
        self.send_email_notification(
            user_email=user_email,
            subject=f"Auction Started: {auction_title}",
            message=f"<p>The auction '{auction_title}' has started!</p><p>Visit the app to start bidding.</p>"
        )
    
    def notify_new_bid(
        self,
        user_id: int,
        user_email: str,
        player_name: str,
        new_bid_amount: float
    ) -> None:
        """Send new bid notification"""
        # Create in-app notification
        self.create_in_app_notification(
            user_id=user_id,
            event=NotificationEvent.BID_PLACED,
            title="New Bid Placed",
            message=f"A new bid of ${new_bid_amount} has been placed on {player_name}"
        )
        
        # Send email
        self.send_email_notification(
            user_email=user_email,
            subject=f"New Bid on {player_name}",
            message=f"<p>A new bid of ${new_bid_amount} has been placed on {player_name}</p>"
        )
    
    def notify_auction_closed(
        self,
        user_id: int,
        user_email: str,
        auction_title: str,
        won: bool = False
    ) -> None:
        """Send auction closed notification"""
        title = "Auction Closed"
        event = NotificationEvent.AUCTION_CLOSED
        
        if won:
            title = "Congratulations!"
            event = NotificationEvent.AUCTION_WON
            message = f"You won a player in the auction '{auction_title}'!"
            email_message = f"<p>Congratulations! You won a player in the auction '{auction_title}'!</p>"
        else:
            message = f"The auction '{auction_title}' has ended."
            email_message = f"<p>The auction '{auction_title}' has ended.</p>"
        
        # Create in-app notification
        self.create_in_app_notification(
            user_id=user_id,
            event=event,
            title=title,
            message=message
        )
        
        # Send email
        self.send_email_notification(
            user_email=user_email,
            subject=title,
            message=email_message
        )
    
    def get_user_notifications(
        self,
        user_id: int,
        unread_only: bool = False,
        offset: int = 0,
        limit: int = 50
    ) -> tuple[List[Notification], int]:
        """Get user notifications"""
        return self.notification_repo.get_user_notifications(
            user_id=user_id,
            unread_only=unread_only,
            offset=offset,
            limit=limit
        )
    
    def mark_notification_as_read(self, notification_id: int) -> Optional[Notification]:
        """Mark notification as read"""
        return self.notification_repo.mark_as_read(notification_id)
    
    def mark_all_as_read(self, user_id: int) -> int:
        """Mark all notifications as read"""
        return self.notification_repo.mark_all_as_read(user_id)
