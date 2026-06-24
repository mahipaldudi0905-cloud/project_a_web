from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class TeamBase(BaseModel):
    """Team base schema"""
    name: str = Field(..., min_length=2, max_length=100)
    budget: float = Field(..., gt=0)
    description: Optional[str] = None


class TeamCreate(TeamBase):
    """Team creation schema"""
    owner_id: int
    logo_url: Optional[str] = None


class TeamUpdate(BaseModel):
    """Team update schema"""
    name: Optional[str] = Field(None, min_length=2)
    budget: Optional[float] = Field(None, gt=0)
    description: Optional[str] = None
    logo_url: Optional[str] = None


class TeamResponse(TeamBase):
    """Team response schema"""
    id: int
    owner_id: int
    wallet_balance: float
    logo_url: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TeamListResponse(BaseModel):
    """Team list response schema"""
    total: int
    page: int
    limit: int
    data: list[TeamResponse]
