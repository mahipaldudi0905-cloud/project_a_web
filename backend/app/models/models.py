from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from app.core.constants import UserRole, UserStatus


class User(SQLModel, table=True):
    """User model"""
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    phone: Optional[str] = Field(default=None, unique=True)
    password_hash: str
    role_id: int = Field(foreign_key="role.id")
    status: str = Field(default=UserStatus.PENDING_VERIFICATION)
    email_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    role: Optional["Role"] = Relationship(back_populates="users")
    wallet: Optional["Wallet"] = Relationship(back_populates="user")
    team: Optional["Team"] = Relationship(back_populates="owner")
    player: Optional["Player"] = Relationship(back_populates="user")
    bids: List["Bid"] = Relationship(back_populates="user")
    transactions: List["Transaction"] = Relationship(back_populates="user")
    notifications: List["Notification"] = Relationship(back_populates="user")


class Role(SQLModel, table=True):
    """User role model"""
    __tablename__ = "role"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None
    
    # Relationships
    users: List[User] = Relationship(back_populates="role")


class Player(SQLModel, table=True):
    """Player model"""
    __tablename__ = "player"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True)
    age: int
    sport: str = Field(index=True)
    city: str
    state: str
    experience_years: int
    base_price: float
    profile_image_url: Optional[str] = None
    video_url: Optional[str] = None
    bio: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: Optional[User] = Relationship(back_populates="player")
    auction_players: List["AuctionPlayer"] = Relationship(back_populates="player")


class Team(SQLModel, table=True):
    """Team model"""
    __tablename__ = "team"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    owner_id: int = Field(foreign_key="users.id", unique=True)
    wallet_balance: float = Field(default=0.0)
    budget: float = Field(default=0.0)
    logo_url: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    owner: Optional[User] = Relationship(back_populates="team")
    bids: List["Bid"] = Relationship(back_populates="team")
    auction_players: List["AuctionPlayer"] = Relationship(back_populates="winning_team")


class Auction(SQLModel, table=True):
    """Auction model"""
    __tablename__ = "auction"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    status: str = Field(default="draft")
    minimum_increment: float = Field(default=5000.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    auction_players: List["AuctionPlayer"] = Relationship(back_populates="auction")


class AuctionPlayer(SQLModel, table=True):
    """Auction Player mapping model"""
    __tablename__ = "auction_player"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    auction_id: int = Field(foreign_key="auction.id")
    player_id: int = Field(foreign_key="player.id")
    base_price: float
    current_price: float = Field(default=0.0)
    winner_team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    status: str = Field(default="unsold")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    auction: Optional[Auction] = Relationship(back_populates="auction_players")
    player: Optional[Player] = Relationship(back_populates="auction_players")
    winning_team: Optional[Team] = Relationship(back_populates="auction_players")
    bids: List["Bid"] = Relationship(back_populates="auction_player")


class Bid(SQLModel, table=True):
    """Bid model"""
    __tablename__ = "bid"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    auction_player_id: int = Field(foreign_key="auction_player.id")
    team_id: int = Field(foreign_key="team.id")
    user_id: int = Field(foreign_key="users.id")
    amount: float
    status: str = Field(default="accepted")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    auction_player: Optional[AuctionPlayer] = Relationship(back_populates="bids")
    team: Optional[Team] = Relationship(back_populates="bids")
    user: Optional[User] = Relationship(back_populates="bids")


class Wallet(SQLModel, table=True):
    """Wallet model"""
    __tablename__ = "wallet"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True)
    balance: float = Field(default=0.0)
    locked_balance: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: Optional[User] = Relationship(back_populates="wallet")
    transactions: List["Transaction"] = Relationship(back_populates="wallet")


class Transaction(SQLModel, table=True):
    """Transaction model"""
    __tablename__ = "transaction"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    wallet_id: int = Field(foreign_key="wallet.id")
    user_id: int = Field(foreign_key="users.id")
    amount: float
    transaction_type: str  # deposit, withdrawal, bid, refund
    status: str = Field(default="pending")  # pending, completed, failed
    gateway_reference: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    
    # Relationships
    wallet: Optional[Wallet] = Relationship(back_populates="transactions")
    user: Optional[User] = Relationship(back_populates="transactions")


class Notification(SQLModel, table=True):
    """Notification model"""
    __tablename__ = "notification"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    notification_type: str  # email, sms, whatsapp, in_app
    event: str
    title: str
    message: str
    is_read: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: Optional[User] = Relationship(back_populates="notifications")
