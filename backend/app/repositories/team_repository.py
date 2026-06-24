from typing import Optional, List
from sqlmodel import Session, select
from app.models.models import Team


class TeamRepository:
    """Team repository for database operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_team(self, team: Team) -> Team:
        """Create a new team"""
        self.session.add(team)
        self.session.commit()
        self.session.refresh(team)
        return team
    
    def get_team_by_id(self, team_id: int) -> Optional[Team]:
        """Get team by ID"""
        return self.session.get(Team, team_id)
    
    def get_team_by_owner_id(self, owner_id: int) -> Optional[Team]:
        """Get team by owner ID"""
        statement = select(Team).where(Team.owner_id == owner_id)
        return self.session.exec(statement).first()
    
    def get_team_by_name(self, name: str) -> Optional[Team]:
        """Get team by name"""
        statement = select(Team).where(Team.name == name)
        return self.session.exec(statement).first()
    
    def get_all_teams(
        self,
        offset: int = 0,
        limit: int = 20
    ) -> tuple[List[Team], int]:
        """Get all teams with pagination"""
        query = select(Team)
        total = len(self.session.exec(query).all())
        
        query = query.offset(offset).limit(limit)
        teams = self.session.exec(query).all()
        
        return teams, total
    
    def update_team(self, team_id: int, **kwargs) -> Optional[Team]:
        """Update team"""
        team = self.get_team_by_id(team_id)
        if team:
            for key, value in kwargs.items():
                if hasattr(team, key) and value is not None:
                    setattr(team, key, value)
            self.session.add(team)
            self.session.commit()
            self.session.refresh(team)
        return team
    
    def delete_team(self, team_id: int) -> bool:
        """Delete team"""
        team = self.get_team_by_id(team_id)
        if team:
            self.session.delete(team)
            self.session.commit()
            return True
        return False
    
    def update_wallet_balance(self, team_id: int, amount: float) -> Optional[Team]:
        """Update team wallet balance"""
        team = self.get_team_by_id(team_id)
        if team:
            team.wallet_balance += amount
            self.session.add(team)
            self.session.commit()
            self.session.refresh(team)
        return team
    
    def lock_wallet_balance(self, team_id: int, amount: float) -> bool:
        """Lock wallet balance for bid"""
        team = self.get_team_by_id(team_id)
        if team and team.wallet_balance >= amount:
            team.wallet_balance -= amount
            self.session.add(team)
            self.session.commit()
            return True
        return False
