from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session
from app.schemas.team import (
    TeamCreate,
    TeamUpdate,
    TeamResponse,
    TeamListResponse
)
from app.models.models import Team, Wallet
from app.repositories.team_repository import TeamRepository
from app.repositories.wallet_repository import WalletRepository
from app.db.session import get_db_session
from app.core.exceptions import AppException, to_http_exception, NotFoundException

router = APIRouter(prefix="/api/v1/teams", tags=["teams"])


@router.post("", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(
    request: TeamCreate,
    session: Session = Depends(get_db_session)
):
    """Create a new team"""
    try:
        team_repo = TeamRepository(session)
        wallet_repo = WalletRepository(session)
        
        team = Team(**request.dict())
        team = team_repo.create_team(team)
        
        # Create team wallet
        wallet = Wallet(user_id=request.owner_id, balance=request.budget)
        wallet_repo.create_wallet(wallet)
        
        return team
    except AppException as e:
        raise to_http_exception(e)


@router.get("", response_model=TeamListResponse)
def get_teams(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_db_session)
):
    """Get all teams"""
    try:
        team_repo = TeamRepository(session)
        teams, total = team_repo.get_all_teams(offset=offset, limit=limit)
        return {
            "total": total,
            "page": offset // limit + 1,
            "limit": limit,
            "data": teams
        }
    except AppException as e:
        raise to_http_exception(e)


@router.get("/{team_id}", response_model=TeamResponse)
def get_team(
    team_id: int,
    session: Session = Depends(get_db_session)
):
    """Get team by ID"""
    try:
        team_repo = TeamRepository(session)
        team = team_repo.get_team_by_id(team_id)
        if not team:
            raise NotFoundException("Team not found")
        return team
    except AppException as e:
        raise to_http_exception(e)


@router.put("/{team_id}", response_model=TeamResponse)
def update_team(
    team_id: int,
    request: TeamUpdate,
    session: Session = Depends(get_db_session)
):
    """Update team"""
    try:
        team_repo = TeamRepository(session)
        team = team_repo.update_team(team_id, **request.dict(exclude_unset=True))
        if not team:
            raise NotFoundException("Team not found")
        return team
    except AppException as e:
        raise to_http_exception(e)
