from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data schema"""
    sub: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None


class RegisterRequest(BaseModel):
    """User registration schema"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = None
    password: str = Field(..., min_length=6, max_length=100)
    role: str  # admin, team_owner, player, moderator


class LoginRequest(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str = Field(..., min_length=6)


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema"""
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    """Forgot password request schema"""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Reset password request schema"""
    token: str
    new_password: str = Field(..., min_length=6)


class ChangePasswordRequest(BaseModel):
    """Change password request schema"""
    old_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)
