from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session
from app.services.notification_service import NotificationService
from app.db.session import get_db_session
from app.core.exceptions import AppException, to_http_exception

router = APIRouter(prefix="/api/v1/notifications", tags=["notifications"])


@router.get("")
def get_notifications(
    user_id: int = Query(...),
    unread_only: bool = Query(False),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    session: Session = Depends(get_db_session)
):
    """Get user notifications"""
    try:
        notification_service = NotificationService(session)
        notifications, total = notification_service.get_user_notifications(
            user_id=user_id,
            unread_only=unread_only,
            offset=offset,
            limit=limit
        )
        return {
            "total": total,
            "page": offset // limit + 1,
            "limit": limit,
            "data": notifications
        }
    except AppException as e:
        raise to_http_exception(e)


@router.put("/{notification_id}/read", status_code=status.HTTP_200_OK)
def mark_notification_as_read(
    notification_id: int,
    session: Session = Depends(get_db_session)
):
    """Mark notification as read"""
    try:
        notification_service = NotificationService(session)
        notification = notification_service.mark_notification_as_read(notification_id)
        return {"message": "Notification marked as read", "notification": notification}
    except AppException as e:
        raise to_http_exception(e)


@router.put("/read-all", status_code=status.HTTP_200_OK)
def mark_all_as_read(
    user_id: int = Query(...),
    session: Session = Depends(get_db_session)
):
    """Mark all notifications as read"""
    try:
        notification_service = NotificationService(session)
        count = notification_service.mark_all_as_read(user_id)
        return {"message": f"{count} notifications marked as read"}
    except AppException as e:
        raise to_http_exception(e)
