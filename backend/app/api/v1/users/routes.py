from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session
from app.schemas.user import UserResponse, UserUpdate, UserListResponse
from app.repositories.user_repository import UserRepository
from app.db.session import get_db_session
from app.core.exceptions import AppException, to_http_exception, NotFoundException

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("", response_model=UserListResponse)
def get_users(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_db_session)
):
    """Get all users"""
    try:
        user_repo = UserRepository(session)
        users, total = user_repo.get_all_users(offset=offset, limit=limit)
        return {
            "total": total,
            "page": offset // limit + 1,
            "limit": limit,
            "data": users
        }
    except AppException as e:
        raise to_http_exception(e)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    session: Session = Depends(get_db_session)
):
    """Get user by ID"""
    try:
        user_repo = UserRepository(session)
        user = user_repo.get_user_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        return user
    except AppException as e:
        raise to_http_exception(e)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    request: UserUpdate,
    session: Session = Depends(get_db_session)
):
    """Update user"""
    try:
        user_repo = UserRepository(session)
        user = user_repo.update_user(user_id, **request.dict(exclude_unset=True))
        if not user:
            raise NotFoundException("User not found")
        return user
    except AppException as e:
        raise to_http_exception(e)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    session: Session = Depends(get_db_session)
):
    """Delete user"""
    try:
        user_repo = UserRepository(session)
        success = user_repo.delete_user(user_id)
        if not success:
            raise NotFoundException("User not found")
    except AppException as e:
        raise to_http_exception(e)
