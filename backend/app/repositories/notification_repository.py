from typing import Optional, List
from sqlmodel import Session, select
from app.models.models import Notification


class NotificationRepository:
    """Notification repository for database operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_notification(self, notification: Notification) -> Notification:
        """Create a new notification"""
        self.session.add(notification)
        self.session.commit()
        self.session.refresh(notification)
        return notification
    
    def get_notification_by_id(self, notification_id: int) -> Optional[Notification]:
        """Get notification by ID"""
        return self.session.get(Notification, notification_id)
    
    def get_user_notifications(
        self,
        user_id: int,
        offset: int = 0,
        limit: int = 50,
        unread_only: bool = False
    ) -> tuple[List[Notification], int]:
        """Get notifications for a user"""
        query = select(Notification).where(Notification.user_id == user_id)
        
        if unread_only:
            query = query.where(Notification.is_read == False)
        
        total = len(self.session.exec(query).all())
        
        query = query.order_by(Notification.created_at.desc()).offset(offset).limit(limit)
        notifications = self.session.exec(query).all()
        
        return notifications, total
    
    def mark_as_read(self, notification_id: int) -> Optional[Notification]:
        """Mark notification as read"""
        notification = self.get_notification_by_id(notification_id)
        if notification:
            notification.is_read = True
            self.session.add(notification)
            self.session.commit()
            self.session.refresh(notification)
        return notification
    
    def mark_all_as_read(self, user_id: int) -> int:
        """Mark all notifications as read for a user"""
        query = select(Notification).where(
            (Notification.user_id == user_id) &
            (Notification.is_read == False)
        )
        notifications = self.session.exec(query).all()
        
        for notification in notifications:
            notification.is_read = True
            self.session.add(notification)
        
        self.session.commit()
        return len(notifications)
    
    def delete_notification(self, notification_id: int) -> bool:
        """Delete notification"""
        notification = self.get_notification_by_id(notification_id)
        if notification:
            self.session.delete(notification)
            self.session.commit()
            return True
        return False
