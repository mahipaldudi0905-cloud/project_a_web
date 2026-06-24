from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import NullPool
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)

settings = get_settings()

# Create engine for MySQL
# Using aiomysql for async support
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
)


def create_db_and_tables():
    """Create all database tables"""
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables created successfully")


def get_session() -> Session:
    """Get database session"""
    with Session(engine) as session:
        yield session


def init_db():
    """Initialize database with default roles"""
    from app.models.models import Role
    from app.core.constants import UserRole
    
    session = Session(engine)
    try:
        # Check if roles already exist
        existing_roles = session.query(Role).all()
        if existing_roles:
            logger.info("Roles already exist in database")
            return
        
        # Create default roles
        roles = [
            Role(name=UserRole.ADMIN, description="Administrator role"),
            Role(name=UserRole.TEAM_OWNER, description="Team owner role"),
            Role(name=UserRole.PLAYER, description="Player role"),
            Role(name=UserRole.MODERATOR, description="Moderator role"),
        ]
        
        for role in roles:
            session.add(role)
        
        session.commit()
        logger.info("Default roles created successfully")
        
    except Exception as e:
        session.rollback()
        logger.error(f"Error initializing database: {e}")
        raise
    finally:
        session.close()
