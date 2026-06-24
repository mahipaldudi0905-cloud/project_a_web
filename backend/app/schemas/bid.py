from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class BidBase(BaseModel):
    """Bid base schema"""
    amount: float = Field(..., gt=0)


class BidCreate(BidBase):
    """Bid creation schema"""
    auction_player_id: int
    team_id: int


class BidResponse(BaseModel):
    """Bid response schema"""
    id: int
    auction_player_id: int
    team_id: int
    user_id: int
    amount: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class BidHistoryResponse(BaseModel):
    """Bid history response schema"""
    total: int
    page: int
    limit: int
    data: list[BidResponse]
