from typing import Optional, List
from sqlmodel import Session
from app.models.models import Auction, AuctionPlayer, Bid
from app.core.exceptions import (
    NotFoundException,
    AuctionException,
    ValidationException
)
from app.repositories.auction_repository import (
    AuctionRepository,
    AuctionPlayerRepository
)
from app.repositories.bid_repository import BidRepository
from app.core.constants import (
    AuctionStatus,
    AUTO_EXTENSION_THRESHOLD_SECONDS,
    AUTO_EXTENSION_DURATION_SECONDS,
    MIN_BID_INCREMENT_PERCENTAGE
)
from datetime import datetime, timedelta


class AuctionService:
    """Auction service"""
    
    def __init__(self, session: Session):
        self.session = session
        self.auction_repo = AuctionRepository(session)
        self.auction_player_repo = AuctionPlayerRepository(session)
        self.bid_repo = BidRepository(session)
    
    def create_auction(
        self,
        title: str,
        description: Optional[str],
        start_time: datetime,
        end_time: datetime,
        minimum_increment: float
    ) -> Auction:
        """Create a new auction"""
        if start_time >= end_time:
            raise ValidationException("Start time must be before end time")
        
        auction = Auction(
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            minimum_increment=minimum_increment,
            status=AuctionStatus.DRAFT
        )
        
        return self.auction_repo.create_auction(auction)
    
    def start_auction(self, auction_id: int) -> Auction:
        """Start an auction"""
        auction = self.auction_repo.get_auction_by_id(auction_id)
        
        if not auction:
            raise NotFoundException("Auction not found")
        
        if auction.status != AuctionStatus.DRAFT:
            raise AuctionException(f"Cannot start auction in {auction.status} status")
        
        return self.auction_repo.update_auction(
            auction_id,
            status=AuctionStatus.LIVE
        )
    
    def close_auction(self, auction_id: int) -> Auction:
        """Close an auction"""
        auction = self.auction_repo.get_auction_by_id(auction_id)
        
        if not auction:
            raise NotFoundException("Auction not found")
        
        if auction.status != AuctionStatus.LIVE:
            raise AuctionException(f"Cannot close auction in {auction.status} status")
        
        return self.auction_repo.update_auction(
            auction_id,
            status=AuctionStatus.CLOSED
        )
    
    def cancel_auction(self, auction_id: int) -> Auction:
        """Cancel an auction"""
        auction = self.auction_repo.get_auction_by_id(auction_id)
        
        if not auction:
            raise NotFoundException("Auction not found")
        
        if auction.status == AuctionStatus.CLOSED:
            raise AuctionException("Cannot cancel closed auction")
        
        return self.auction_repo.update_auction(
            auction_id,
            status=AuctionStatus.CANCELLED
        )
    
    def add_player_to_auction(
        self,
        auction_id: int,
        player_id: int,
        base_price: float
    ) -> AuctionPlayer:
        """Add a player to auction"""
        auction = self.auction_repo.get_auction_by_id(auction_id)
        
        if not auction:
            raise NotFoundException("Auction not found")
        
        # Check if player already in auction
        from sqlmodel import select
        query = select(AuctionPlayer).where(
            (AuctionPlayer.auction_id == auction_id) &
            (AuctionPlayer.player_id == player_id)
        )
        if self.session.exec(query).first():
            raise ValidationException("Player already added to this auction")
        
        auction_player = AuctionPlayer(
            auction_id=auction_id,
            player_id=player_id,
            base_price=base_price,
            current_price=base_price,
            status="unsold"
        )
        
        return self.auction_player_repo.create_auction_player(auction_player)
    
    def get_auction_details(self, auction_id: int) -> dict:
        """Get auction details with players and bids"""
        auction = self.auction_repo.get_auction_by_id(auction_id)
        
        if not auction:
            raise NotFoundException("Auction not found")
        
        auction_players, total = self.auction_repo.get_auction_players(auction_id, limit=1000)
        
        players_data = []
        for ap in auction_players:
            bids, _ = self.bid_repo.get_bids_for_player(ap.id, limit=1000)
            players_data.append({
                "id": ap.id,
                "player_id": ap.player_id,
                "base_price": ap.base_price,
                "current_price": ap.current_price,
                "winner_team_id": ap.winner_team_id,
                "status": ap.status,
                "bid_count": len(bids),
                "bids": bids
            })
        
        return {
            "id": auction.id,
            "title": auction.title,
            "description": auction.description,
            "start_time": auction.start_time,
            "end_time": auction.end_time,
            "status": auction.status,
            "minimum_increment": auction.minimum_increment,
            "players": players_data,
            "player_count": len(players_data)
        }


class BidService:
    """Bid service"""
    
    def __init__(self, session: Session):
        self.session = session
        self.bid_repo = BidRepository(session)
        self.auction_player_repo = AuctionPlayerRepository(session)
    
    def place_bid(
        self,
        auction_player_id: int,
        team_id: int,
        user_id: int,
        amount: float
    ) -> Bid:
        """Place a bid on an auction player"""
        auction_player = self.auction_player_repo.get_auction_player_by_id(
            auction_player_id
        )
        
        if not auction_player:
            raise NotFoundException("Auction player not found")
        
        # Check if player is already sold
        if auction_player.status == "sold":
            raise ValidationException("Player already sold")
        
        # Check minimum bid amount
        min_bid_amount = auction_player.current_price + (
            auction_player.current_price * MIN_BID_INCREMENT_PERCENTAGE / 100
        )
        
        if amount < min_bid_amount:
            raise ValidationException(
                f"Bid amount must be at least {min_bid_amount}"
            )
        
        # Create bid
        bid = Bid(
            auction_player_id=auction_player_id,
            team_id=team_id,
            user_id=user_id,
            amount=amount,
            status="accepted"
        )
        
        bid = self.bid_repo.create_bid(bid)
        
        # Update current price
        self.auction_player_repo.update_current_price(
            auction_player_id,
            amount
        )
        
        return bid
    
    def get_bid_history(
        self,
        auction_player_id: int,
        limit: int = 50
    ) -> List[Bid]:
        """Get bid history for a player"""
        bids, _ = self.bid_repo.get_bids_for_player(
            auction_player_id,
            limit=limit
        )
        return bids
    
    def get_highest_bid(self, auction_player_id: int) -> Optional[Bid]:
        """Get highest bid for an auction player"""
        return self.bid_repo.get_highest_bid_for_player(auction_player_id)
