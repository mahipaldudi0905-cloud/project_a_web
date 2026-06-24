from typing import Optional, List
from sqlmodel import Session, select
from app.models.models import Bid


class BidRepository:
    """Bid repository for database operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_bid(self, bid: Bid) -> Bid:
        """Create a new bid"""
        self.session.add(bid)
        self.session.commit()
        self.session.refresh(bid)
        return bid
    
    def get_bid_by_id(self, bid_id: int) -> Optional[Bid]:
        """Get bid by ID"""
        return self.session.get(Bid, bid_id)
    
    def get_bids_for_player(
        self,
        auction_player_id: int,
        offset: int = 0,
        limit: int = 50
    ) -> tuple[List[Bid], int]:
        """Get all bids for an auction player"""
        query = select(Bid).where(Bid.auction_player_id == auction_player_id)
        total = len(self.session.exec(query).all())
        
        query = query.order_by(Bid.created_at.desc()).offset(offset).limit(limit)
        bids = self.session.exec(query).all()
        
        return bids, total
    
    def get_highest_bid_for_player(self, auction_player_id: int) -> Optional[Bid]:
        """Get highest bid for an auction player"""
        query = select(Bid).where(
            Bid.auction_player_id == auction_player_id
        ).order_by(Bid.amount.desc()).limit(1)
        return self.session.exec(query).first()
    
    def get_bids_by_team(
        self,
        team_id: int,
        offset: int = 0,
        limit: int = 50
    ) -> tuple[List[Bid], int]:
        """Get all bids placed by a team"""
        query = select(Bid).where(Bid.team_id == team_id)
        total = len(self.session.exec(query).all())
        
        query = query.order_by(Bid.created_at.desc()).offset(offset).limit(limit)
        bids = self.session.exec(query).all()
        
        return bids, total
    
    def update_bid(self, bid_id: int, **kwargs) -> Optional[Bid]:
        """Update bid"""
        bid = self.get_bid_by_id(bid_id)
        if bid:
            for key, value in kwargs.items():
                if hasattr(bid, key) and value is not None:
                    setattr(bid, key, value)
            self.session.add(bid)
            self.session.commit()
            self.session.refresh(bid)
        return bid
    
    def delete_bid(self, bid_id: int) -> bool:
        """Delete bid"""
        bid = self.get_bid_by_id(bid_id)
        if bid:
            self.session.delete(bid)
            self.session.commit()
            return True
        return False
    
    def get_total_bid_amount_by_team(self, team_id: int, auction_id: int) -> float:
        """Get total amount bid by team in an auction"""
        query = select(Bid).join(Bid.auction_player).where(
            (Bid.team_id == team_id)
        )
        bids = self.session.exec(query).all()
        return sum(bid.amount for bid in bids if bid.auction_player)
