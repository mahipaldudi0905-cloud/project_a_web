from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class AuctionBase(BaseModel):
    """Auction base schema"""
    title: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    minimum_increment: float = Field(default=5000.0, gt=0)


class AuctionCreate(AuctionBase):
    """Auction creation schema"""
    pass


class AuctionUpdate(BaseModel):
    """Auction update schema"""
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    minimum_increment: Optional[float] = Field(None, gt=0)


class AuctionResponse(AuctionBase):
    """Auction response schema"""
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AuctionListResponse(BaseModel):
    """Auction list response schema"""
    total: int
    page: int
    limit: int
    data: list[AuctionResponse]


class AuctionPlayerBase(BaseModel):
    """Auction player base schema"""
    auction_id: int
    player_id: int
    base_price: float = Field(..., gt=0)


class AuctionPlayerCreate(AuctionPlayerBase):
    """Auction player creation schema"""
    pass


class AuctionPlayerResponse(BaseModel):
    """Auction player response schema"""
    id: int
    auction_id: int
    player_id: int
    base_price: float
    current_price: float
    winner_team_id: Optional[int]
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AuctionPlayerListResponse(BaseModel):
    """Auction player list response schema"""
    total: int
    page: int
    limit: int
    data: list[AuctionPlayerResponse]
