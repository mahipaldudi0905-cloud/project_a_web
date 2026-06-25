from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.db.database import create_db_and_tables, init_db
from app.api.v1.auth.routes import router as auth_router
from app.api.v1.users.routes import router as users_router
from app.api.v1.players.routes import router as players_router
from app.api.v1.teams.routes import router as teams_router
from app.api.v1.auctions.routes import router as auctions_router
from app.api.v1.bids.routes import router as bids_router
from app.api.v1.wallets.routes import router as wallets_router
from app.api.v1.payments.routes import router as payments_router
from app.api.v1.notifications.routes import router as notifications_router
from app.api.v1.reports.routes import router as reports_router
import logging

settings = get_settings()

# Setup logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Cricket Auction Platform API"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    """Initialize database on startup"""
    create_db_and_tables()
    init_db()


# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(players_router)
app.include_router(teams_router)
app.include_router(auctions_router)
app.include_router(bids_router)
app.include_router(wallets_router)
app.include_router(payments_router)
app.include_router(notifications_router)
app.include_router(reports_router)


@app.get("/")
def read_root():
    """Welcome endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


@app.exception_handler(HTTPException)
def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return {
        "status": "error",
        "code": exc.status_code,
        "detail": exc.detail
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
