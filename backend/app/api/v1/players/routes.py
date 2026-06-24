from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session
from app.schemas.player import (
    PlayerCreate,
    PlayerUpdate,
    PlayerResponse,
    PlayerListResponse
)
from app.models.models import Player
from app.repositories.player_repository import PlayerRepository
from app.db.session import get_db_session
from app.core.exceptions import AppException, to_http_exception, NotFoundException

router = APIRouter(prefix="/api/v1/players", tags=["players"])


@router.post("", response_model=PlayerResponse, status_code=status.HTTP_201_CREATED)
def create_player(
    request: PlayerCreate,
    session: Session = Depends(get_db_session)
):
    """Create a new player"""
    try:
        player_repo = PlayerRepository(session)
        player = Player(**request.dict())
        player = player_repo.create_player(player)
        return player
    except AppException as e:
        raise to_http_exception(e)


@router.get("", response_model=PlayerListResponse)
def get_players(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sport: str = Query(None),
    city: str = Query(None),
    session: Session = Depends(get_db_session)
):
    """Get all players with filters"""
    try:
        player_repo = PlayerRepository(session)
        players, total = player_repo.get_all_players(
            offset=offset,
            limit=limit,
            sport=sport,
            city=city
        )
        return {
            "total": total,
            "page": offset // limit + 1,
            "limit": limit,
            "data": players
        }
    except AppException as e:
        raise to_http_exception(e)


@router.get("/{player_id}", response_model=PlayerResponse)
def get_player(
    player_id: int,
    session: Session = Depends(get_db_session)
):
    """Get player by ID"""
    try:
        player_repo = PlayerRepository(session)
        player = player_repo.get_player_by_id(player_id)
        if not player:
            raise NotFoundException("Player not found")
        return player
    except AppException as e:
        raise to_http_exception(e)


@router.put("/{player_id}", response_model=PlayerResponse)
def update_player(
    player_id: int,
    request: PlayerUpdate,
    session: Session = Depends(get_db_session)
):
    """Update player"""
    try:
        player_repo = PlayerRepository(session)
        player = player_repo.update_player(player_id, **request.dict(exclude_unset=True))
        if not player:
            raise NotFoundException("Player not found")
        return player
    except AppException as e:
        raise to_http_exception(e)


@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_player(
    player_id: int,
    session: Session = Depends(get_db_session)
):
    """Delete player"""
    try:
        player_repo = PlayerRepository(session)
        success = player_repo.delete_player(player_id)
        if not success:
            raise NotFoundException("Player not found")
    except AppException as e:
        raise to_http_exception(e)
