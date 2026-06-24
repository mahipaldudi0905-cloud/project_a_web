from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlmodel import Session
from app.models.models import User, Role
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.core.exceptions import (
    AuthenticationException,
    ConflictException,
    NotFoundException,
    ValidationException
)
from app.repositories.user_repository import UserRepository
from app.core.constants import UserRole, UserStatus


class AuthService:
    """Authentication service"""
    
    def __init__(self, session: Session):
        self.session = session
        self.user_repo = UserRepository(session)
    
    def register(
        self,
        name: str,
        email: str,
        password: str,
        phone: Optional[str] = None,
        role: str = UserRole.PLAYER
    ) -> User:
        """Register a new user"""
        # Check if user already exists
        if self.user_repo.get_user_by_email(email):
            raise ConflictException("Email already registered")
        
        if phone and self.user_repo.get_user_by_phone(phone):
            raise ConflictException("Phone number already registered")
        
        # Get role
        role_query = self.session.query(Role).filter(Role.name == role).first()
        if not role_query:
            raise NotFoundException(f"Role {role} not found")
        
        # Create user
        user = User(
            name=name,
            email=email,
            phone=phone,
            password_hash=get_password_hash(password),
            role_id=role_query.id,
            status=UserStatus.PENDING_VERIFICATION
        )
        
        return self.user_repo.create_user(user)
    
    def login(self, email: str, password: str) -> dict:
        """Authenticate user and return tokens"""
        user = self.user_repo.get_user_by_email(email)
        
        if not user or not verify_password(password, user.password_hash):
            raise AuthenticationException("Invalid email or password")
        
        if user.status == UserStatus.BANNED:
            raise AuthenticationException("User account is banned")
        
        # Create tokens
        access_token = create_access_token(
            data={
                "sub": user.email,
                "user_id": user.id,
                "role": user.role.name
            }
        )
        refresh_token = create_refresh_token(
            data={
                "sub": user.email,
                "user_id": user.id
            }
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    def refresh_access_token(self, refresh_token: str) -> dict:
        """Refresh access token"""
        payload = decode_token(refresh_token)
        
        if not payload or not payload.get("user_id"):
            raise AuthenticationException("Invalid refresh token")
        
        user = self.user_repo.get_user_by_id(payload["user_id"])
        
        if not user:
            raise NotFoundException("User not found")
        
        # Create new access token
        access_token = create_access_token(
            data={
                "sub": user.email,
                "user_id": user.id,
                "role": user.role.name
            }
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    
    def verify_email(self, user_id: int) -> User:
        """Verify user email"""
        user = self.user_repo.verify_email(user_id)
        if not user:
            raise NotFoundException("User not found")
        return user
    
    def change_password(
        self,
        user_id: int,
        old_password: str,
        new_password: str
    ) -> User:
        """Change user password"""
        user = self.user_repo.get_user_by_id(user_id)
        
        if not user:
            raise NotFoundException("User not found")
        
        if not verify_password(old_password, user.password_hash):
            raise AuthenticationException("Old password is incorrect")
        
        if old_password == new_password:
            raise ValidationException("New password must be different from old password")
        
        return self.user_repo.update_user(
            user_id,
            password_hash=get_password_hash(new_password)
        )
