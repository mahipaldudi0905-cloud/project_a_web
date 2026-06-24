from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class PlayerBase(BaseModel):
    """Player base schema"""
    age: int = Field(..., ge=15, le=60)
    sport: str = Field(..., min_length=2, max_length=50)
    city: str = Field(..., min_length=2)
    state: str = Field(..., min_length=2)
    experience_years: int = Field(..., ge=0)
    base_price: float = Field(..., gt=0)
    bio: Optional[str] = None


class PlayerCreate(PlayerBase):
    """Player creation schema"""
    user_id: int
    profile_image_url: Optional[str] = None
    video_url: Optional[str] = None


class PlayerUpdate(BaseModel):
    """Player update schema"""
    age: Optional[int] = Field(None, ge=15, le=60)
    sport: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    experience_years: Optional[int] = Field(None, ge=0)
    base_price: Optional[float] = Field(None, gt=0)
    bio: Optional[str] = None
    profile_image_url: Optional[str] = None
    video_url: Optional[str] = None


class PlayerResponse(PlayerBase):
    """Player response schema"""
    id: int
    user_id: int
    profile_image_url: Optional[str]
    video_url: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PlayerListResponse(BaseModel):
    """Player list response schema"""
    total: int
    page: int
    limit: int
    data: list[PlayerResponse]
