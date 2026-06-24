from typing import Optional, List
from sqlmodel import Session, select
from app.models.models import Auction, AuctionPlayer
from app.core.constants import AuctionStatus


class AuctionRepository:
    """Auction repository for database operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_auction(self, auction: Auction) -> Auction:
        """Create a new auction"""
        self.session.add(auction)
        self.session.commit()
        self.session.refresh(auction)
        return auction
    
    def get_auction_by_id(self, auction_id: int) -> Optional[Auction]:
        """Get auction by ID"""
        return self.session.get(Auction, auction_id)
    
    def get_all_auctions(
        self,
        offset: int = 0,
        limit: int = 20,
        status: Optional[str] = None
    ) -> tuple[List[Auction], int]:
        """Get all auctions with pagination"""
        query = select(Auction)
        
        if status:
            query = query.where(Auction.status == status)
        
        total = len(self.session.exec(query).all())
        
        query = query.offset(offset).limit(limit)
        auctions = self.session.exec(query).all()
        
        return auctions, total
    
    def update_auction(self, auction_id: int, **kwargs) -> Optional[Auction]:
        """Update auction"""
        auction = self.get_auction_by_id(auction_id)
        if auction:
            for key, value in kwargs.items():
                if hasattr(auction, key) and value is not None:
                    setattr(auction, key, value)
            self.session.add(auction)
            self.session.commit()
            self.session.refresh(auction)
        return auction
    
    def delete_auction(self, auction_id: int) -> bool:
        """Delete auction"""
        auction = self.get_auction_by_id(auction_id)
        if auction:
            self.session.delete(auction)
            self.session.commit()
            return True
        return False
    
    def get_auction_players(
        self,
        auction_id: int,
        offset: int = 0,
        limit: int = 20
    ) -> tuple[List[AuctionPlayer], int]:
        """Get players in an auction"""
        query = select(AuctionPlayer).where(AuctionPlayer.auction_id == auction_id)
        total = len(self.session.exec(query).all())
        
        query = query.offset(offset).limit(limit)
        players = self.session.exec(query).all()
        
        return players, total


class AuctionPlayerRepository:
    """Auction Player repository for database operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_auction_player(self, auction_player: AuctionPlayer) -> AuctionPlayer:
        """Add player to auction"""
        self.session.add(auction_player)
        self.session.commit()
        self.session.refresh(auction_player)
        return auction_player
    
    def get_auction_player_by_id(self, auction_player_id: int) -> Optional[AuctionPlayer]:
        """Get auction player by ID"""
        return self.session.get(AuctionPlayer, auction_player_id)
    
    def update_auction_player(
        self,
        auction_player_id: int,
        **kwargs
    ) -> Optional[AuctionPlayer]:
        """Update auction player"""
        ap = self.get_auction_player_by_id(auction_player_id)
        if ap:
            for key, value in kwargs.items():
                if hasattr(ap, key) and value is not None:
                    setattr(ap, key, value)
            self.session.add(ap)
            self.session.commit()
            self.session.refresh(ap)
        return ap
    
    def update_current_price(
        self,
        auction_player_id: int,
        new_price: float
    ) -> Optional[AuctionPlayer]:
        """Update current price for auction player"""
        return self.update_auction_player(auction_player_id, current_price=new_price)
    
    def set_winner(
        self,
        auction_player_id: int,
        team_id: int
    ) -> Optional[AuctionPlayer]:
        """Set winning team for auction player"""
        return self.update_auction_player(
            auction_player_id,
            winner_team_id=team_id,
            status="sold"
        )
    
    def delete_auction_player(self, auction_player_id: int) -> bool:
        """Remove player from auction"""
        ap = self.get_auction_player_by_id(auction_player_id)
        if ap:
            self.session.delete(ap)
            self.session.commit()
            return True
        return False
