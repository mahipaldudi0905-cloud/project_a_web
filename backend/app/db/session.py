from contextlib import asynccontextmanager
from sqlmodel import Session
from app.db.database import engine


@asynccontextmanager
async def get_async_session():
    """Get async database session"""
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


def get_db_session():
    """Get database session for dependency injection"""
    with Session(engine) as session:
        yield session
