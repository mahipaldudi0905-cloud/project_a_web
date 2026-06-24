from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    RefreshTokenRequest,
    TokenResponse,
    ChangePasswordRequest
)
from app.services.auth_service import AuthService
from app.db.session import get_db_session
from app.core.exceptions import AppException, to_http_exception
from app.core.security import decode_token

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


def get_current_user(token: str, session: Session = Depends(get_db_session)):
    """Dependency to get current user from token"""
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    payload = decode_token(token.replace("Bearer ", ""))
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return payload


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
def register(
    request: RegisterRequest,
    session: Session = Depends(get_db_session)
):
    """Register a new user"""
    try:
        auth_service = AuthService(session)
        user = auth_service.register(
            name=request.name,
            email=request.email,
            password=request.password,
            phone=request.phone,
            role=request.role
        )
        return {"id": user.id, "email": user.email, "message": "Registration successful"}
    except AppException as e:
        raise to_http_exception(e)


@router.post("/login", response_model=TokenResponse)
def login(
    request: LoginRequest,
    session: Session = Depends(get_db_session)
):
    """Login user"""
    try:
        auth_service = AuthService(session)
        tokens = auth_service.login(request.email, request.password)
        return tokens
    except AppException as e:
        raise to_http_exception(e)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    request: RefreshTokenRequest,
    session: Session = Depends(get_db_session)
):
    """Refresh access token"""
    try:
        auth_service = AuthService(session)
        tokens = auth_service.refresh_access_token(request.refresh_token)
        return tokens
    except AppException as e:
        raise to_http_exception(e)


@router.post("/change-password", response_model=dict)
def change_password(
    request: ChangePasswordRequest,
    token: str = Depends(lambda: None),
    session: Session = Depends(get_db_session)
):
    """Change user password"""
    try:
        payload = decode_token(token.replace("Bearer ", ""))
        if not payload:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        user_id = payload.get("user_id")
        auth_service = AuthService(session)
        auth_service.change_password(user_id, request.old_password, request.new_password)
        return {"message": "Password changed successfully"}
    except AppException as e:
        raise to_http_exception(e)
