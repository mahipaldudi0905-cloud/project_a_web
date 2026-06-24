from typing import Optional, List
from sqlmodel import Session, select
from app.models.models import User
from app.core.constants import UserStatus


class UserRepository:
    """User repository for database operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_user(self, user: User) -> User:
        """Create a new user"""
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.session.get(User, user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()
    
    def get_user_by_phone(self, phone: str) -> Optional[User]:
        """Get user by phone"""
        statement = select(User).where(User.phone == phone)
        return self.session.exec(statement).first()
    
    def get_all_users(
        self,
        offset: int = 0,
        limit: int = 20,
        status: Optional[str] = None
    ) -> tuple[List[User], int]:
        """Get all users with pagination"""
        query = select(User)
        
        if status:
            query = query.where(User.status == status)
        
        total = len(self.session.exec(query).all())
        
        query = query.offset(offset).limit(limit)
        users = self.session.exec(query).all()
        
        return users, total
    
    def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        """Update user"""
        user = self.get_user_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key) and value is not None:
                    setattr(user, key, value)
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
        return user
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user"""
        user = self.get_user_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False
    
    def verify_email(self, user_id: int) -> Optional[User]:
        """Verify user email"""
        return self.update_user(user_id, email_verified=True, status=UserStatus.ACTIVE)
