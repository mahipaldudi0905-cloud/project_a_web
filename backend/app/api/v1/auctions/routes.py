from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session
from app.schemas.auction import (
    AuctionCreate,
    AuctionUpdate,
    AuctionResponse,
    AuctionListResponse,
    AuctionPlayerCreate,
    AuctionPlayerResponse
)
from app.models.models import Auction, AuctionPlayer
from app.services.auction_service import AuctionService
from app.repositories.auction_repository import AuctionRepository, AuctionPlayerRepository
from app.db.session import get_db_session
from app.core.exceptions import AppException, to_http_exception, NotFoundException

router = APIRouter(prefix="/api/v1/auctions", tags=["auctions"])


@router.post("", response_model=AuctionResponse, status_code=status.HTTP_201_CREATED)
def create_auction(
    request: AuctionCreate,
    session: Session = Depends(get_db_session)
):
    """Create a new auction"""
    try:
        auction_service = AuctionService(session)
        auction = auction_service.create_auction(
            title=request.title,
            description=request.description,
            start_time=request.start_time,
            end_time=request.end_time,
            minimum_increment=request.minimum_increment
        )
        return auction
    except AppException as e:
        raise to_http_exception(e)


@router.get("", response_model=AuctionListResponse)
def get_auctions(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: str = Query(None),
    session: Session = Depends(get_db_session)
):
    """Get all auctions"""
    try:
        auction_repo = AuctionRepository(session)
        auctions, total = auction_repo.get_all_auctions(
            offset=offset,
            limit=limit,
            status=status
        )
        return {
            "total": total,
            "page": offset // limit + 1,
            "limit": limit,
            "data": auctions
        }
    except AppException as e:
        raise to_http_exception(e)


@router.get("/{auction_id}", response_model=dict)
def get_auction(
    auction_id: int,
    session: Session = Depends(get_db_session)
):
    """Get auction details with players"""
    try:
        auction_service = AuctionService(session)
        auction = auction_service.get_auction_details(auction_id)
        return auction
    except AppException as e:
        raise to_http_exception(e)


@router.put("/{auction_id}", response_model=AuctionResponse)
def update_auction(
    auction_id: int,
    request: AuctionUpdate,
    session: Session = Depends(get_db_session)
):
    """Update auction"""
    try:
        auction_repo = AuctionRepository(session)
        auction = auction_repo.update_auction(auction_id, **request.dict(exclude_unset=True))
        if not auction:
            raise NotFoundException("Auction not found")
        return auction
    except AppException as e:
        raise to_http_exception(e)


@router.post("/{auction_id}/start", response_model=AuctionResponse)
def start_auction(
    auction_id: int,
    session: Session = Depends(get_db_session)
):
    """Start an auction"""
    try:
        auction_service = AuctionService(session)
        auction = auction_service.start_auction(auction_id)
        return auction
    except AppException as e:
        raise to_http_exception(e)


@router.post("/{auction_id}/close", response_model=AuctionResponse)
def close_auction(
    auction_id: int,
    session: Session = Depends(get_db_session)
):
    """Close an auction"""
    try:
        auction_service = AuctionService(session)
        auction = auction_service.close_auction(auction_id)
        return auction
    except AppException as e:
        raise to_http_exception(e)


@router.post("/{auction_id}/cancel", response_model=AuctionResponse)
def cancel_auction(
    auction_id: int,
    session: Session = Depends(get_db_session)
):
    """Cancel an auction"""
    try:
        auction_service = AuctionService(session)
        auction = auction_service.cancel_auction(auction_id)
        return auction
    except AppException as e:
        raise to_http_exception(e)


@router.post("/players", response_model=AuctionPlayerResponse, status_code=status.HTTP_201_CREATED)
def add_player_to_auction(
    request: AuctionPlayerCreate,
    session: Session = Depends(get_db_session)
):
    """Add player to auction"""
    try:
        auction_service = AuctionService(session)
        auction_player = auction_service.add_player_to_auction(
            auction_id=request.auction_id,
            player_id=request.player_id,
            base_price=request.base_price
        )
        return auction_player
    except AppException as e:
        raise to_http_exception(e)


@router.get("/players/{auction_player_id}", response_model=AuctionPlayerResponse)
def get_auction_player(
    auction_player_id: int,
    session: Session = Depends(get_db_session)
):
    """Get auction player"""
    try:
        auction_player_repo = AuctionPlayerRepository(session)
        ap = auction_player_repo.get_auction_player_by_id(auction_player_id)
        if not ap:
            raise NotFoundException("Auction player not found")
        return ap
    except AppException as e:
        raise to_http_exception(e)
