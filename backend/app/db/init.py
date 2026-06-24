from sqlmodel import Session
from app.models.models import Role
from app.core.constants import UserRole
from app.db.database import engine


def init_default_roles():
    """Initialize default roles in database"""
    session = Session(engine)
    
    try:
        # Check existing roles
        existing_roles = session.query(Role).all()
        if existing_roles:
            print("Roles already exist")
            return
        
        # Create default roles
        roles = [
            Role(name=UserRole.ADMIN, description="Administrator"),
            Role(name=UserRole.TEAM_OWNER, description="Team Owner"),
            Role(name=UserRole.PLAYER, description="Player"),
            Role(name=UserRole.MODERATOR, description="Moderator"),
        ]
        
        for role in roles:
            session.add(role)
            print(f"Created role: {role.name}")
        
        session.commit()
        print("Default roles initialized successfully")
        
    except Exception as e:
        session.rollback()
        print(f"Error initializing roles: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    init_default_roles()
