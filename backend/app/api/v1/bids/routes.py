from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session
from app.schemas.bid import (
    BidCreate,
    BidResponse,
    BidHistoryResponse
)
from app.models.models import Bid
from app.services.auction_service import BidService
from app.repositories.bid_repository import BidRepository
from app.db.session import get_db_session
from app.core.exceptions import AppException, to_http_exception, NotFoundException

router = APIRouter(prefix="/api/v1/bids", tags=["bids"])


@router.post("", response_model=BidResponse, status_code=status.HTTP_201_CREATED)
def place_bid(
    request: BidCreate,
    session: Session = Depends(get_db_session)
):
    """Place a bid"""
    try:
        bid_service = BidService(session)
        bid = bid_service.place_bid(
            auction_player_id=request.auction_player_id,
            team_id=request.team_id,
            user_id=1,  # Should come from auth token
            amount=request.amount
        )
        return bid
    except AppException as e:
        raise to_http_exception(e)


@router.get("", response_model=BidHistoryResponse)
def get_bids(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    session: Session = Depends(get_db_session)
):
    """Get all bids"""
    try:
        bid_repo = BidRepository(session)
        from sqlmodel import select
        query = select(Bid)
        total = len(session.exec(query).all())
        
        query = query.offset(offset).limit(limit).order_by(Bid.created_at.desc())
        bids = session.exec(query).all()
        
        return {
            "total": total,
            "page": offset // limit + 1,
            "limit": limit,
            "data": bids
        }
    except AppException as e:
        raise to_http_exception(e)


@router.get("/history/{player_id}", response_model=BidHistoryResponse)
def get_bid_history(
    player_id: int,
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    session: Session = Depends(get_db_session)
):
    """Get bid history for a player"""
    try:
        bid_service = BidService(session)
        bid_repo = BidRepository(session)
        
        bids, total = bid_repo.get_bids_for_player(
            player_id,
            offset=offset,
            limit=limit
        )
        
        return {
            "total": total,
            "page": offset // limit + 1,
            "limit": limit,
            "data": bids
        }
    except AppException as e:
        raise to_http_exception(e)
