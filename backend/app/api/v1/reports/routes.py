from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from app.db.session import get_db_session

router = APIRouter(prefix="/api/v1/reports", tags=["reports"])


@router.get("/auction")
def get_auction_reports(
    auction_id: int = Query(...),
    session: Session = Depends(get_db_session)
):
    """Get auction reports"""
    try:
        from app.repositories.auction_repository import AuctionRepository
        
        auction_repo = AuctionRepository(session)
        auction = auction_repo.get_auction_by_id(auction_id)
        
        if not auction:
            return {"error": "Auction not found"}
        
        auction_players, _ = auction_repo.get_auction_players(auction_id, limit=1000)
        
        total_amount = sum(ap.current_price for ap in auction_players)
        sold_count = len([ap for ap in auction_players if ap.status == "sold"])
        
        return {
            "auction_id": auction.id,
            "title": auction.title,
            "status": auction.status,
            "total_players": len(auction_players),
            "sold_players": sold_count,
            "unsold_players": len(auction_players) - sold_count,
            "total_amount": total_amount,
            "average_price": total_amount / len(auction_players) if auction_players else 0
        }
    
    except Exception as e:
        return {"error": str(e)}


@router.get("/revenue")
def get_revenue_reports(
    session: Session = Depends(get_db_session)
):
    """Get revenue reports"""
    try:
        from app.models.models import Transaction
        from sqlmodel import select
        from app.core.constants import TransactionStatus
        
        query = select(Transaction).where(
            Transaction.status == TransactionStatus.COMPLETED
        )
        transactions = session.exec(query).all()
        
        total_revenue = sum(t.amount for t in transactions)
        completed_count = len(transactions)
        
        return {
            "total_revenue": total_revenue,
            "total_transactions": completed_count,
            "average_transaction": total_revenue / completed_count if completed_count > 0 else 0
        }
    
    except Exception as e:
        return {"error": str(e)}


@router.get("/user")
def get_user_reports(
    session: Session = Depends(get_db_session)
):
    """Get user reports"""
    try:
        from app.models.models import User
        from sqlmodel import select
        
        query = select(User)
        users = session.exec(query).all()
        
        return {
            "total_users": len(users),
            "active_users": len([u for u in users if u.status == "active"]),
            "pending_verification": len([u for u in users if u.status == "pending_verification"])
        }
    
    except Exception as e:
        return {"error": str(e)}
