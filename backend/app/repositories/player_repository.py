from typing import Optional, List
from sqlmodel import Session, select
from app.models.models import Player


class PlayerRepository:
    """Player repository for database operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_player(self, player: Player) -> Player:
        """Create a new player"""
        self.session.add(player)
        self.session.commit()
        self.session.refresh(player)
        return player
    
    def get_player_by_id(self, player_id: int) -> Optional[Player]:
        """Get player by ID"""
        return self.session.get(Player, player_id)
    
    def get_player_by_user_id(self, user_id: int) -> Optional[Player]:
        """Get player by user ID"""
        statement = select(Player).where(Player.user_id == user_id)
        return self.session.exec(statement).first()
    
    def get_all_players(
        self,
        offset: int = 0,
        limit: int = 20,
        sport: Optional[str] = None,
        city: Optional[str] = None
    ) -> tuple[List[Player], int]:
        """Get all players with filters"""
        query = select(Player)
        
        if sport:
            query = query.where(Player.sport == sport)
        if city:
            query = query.where(Player.city == city)
        
        total = len(self.session.exec(query).all())
        
        query = query.offset(offset).limit(limit)
        players = self.session.exec(query).all()
        
        return players, total
    
    def update_player(self, player_id: int, **kwargs) -> Optional[Player]:
        """Update player"""
        player = self.get_player_by_id(player_id)
        if player:
            for key, value in kwargs.items():
                if hasattr(player, key) and value is not None:
                    setattr(player, key, value)
            self.session.add(player)
            self.session.commit()
            self.session.refresh(player)
        return player
    
    def delete_player(self, player_id: int) -> bool:
        """Delete player"""
        player = self.get_player_by_id(player_id)
        if player:
            self.session.delete(player)
            self.session.commit()
            return True
        return False
    
    def search_players(
        self,
        keyword: str,
        offset: int = 0,
        limit: int = 20
    ) -> tuple[List[Player], int]:
        """Search players by name or location"""
        from app.models.models import User
        
        query = select(Player).join(User).where(
            (User.name.contains(keyword)) |
            (Player.sport.contains(keyword)) |
            (Player.city.contains(keyword))
        )
        
        total = len(self.session.exec(query).all())
        
        query = query.offset(offset).limit(limit)
        players = self.session.exec(query).all()
        
        return players, total
