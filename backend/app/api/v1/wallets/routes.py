from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session
from app.schemas.wallet import (
    WalletResponse,
    DepositRequest,
    WithdrawRequest,
    TransactionHistoryResponse
)
from app.services.wallet_service import WalletService
from app.db.session import get_db_session
from app.core.exceptions import AppException, to_http_exception

router = APIRouter(prefix="/api/v1/wallet", tags=["wallet"])


@router.get("", response_model=WalletResponse)
def get_wallet(
    user_id: int = Query(...),
    session: Session = Depends(get_db_session)
):
    """Get user wallet"""
    try:
        wallet_service = WalletService(session)
        wallet = wallet_service.get_wallet(user_id)
        return {
            **wallet.dict(),
            "available_balance": wallet.balance
        }
    except AppException as e:
        raise to_http_exception(e)


@router.post("/deposit", status_code=status.HTTP_201_CREATED)
def deposit_funds(
    user_id: int = Query(...),
    request: DepositRequest = None,
    session: Session = Depends(get_db_session)
):
    """Deposit funds to wallet"""
    try:
        wallet_service = WalletService(session)
        transaction = wallet_service.deposit_funds(
            user_id=user_id,
            amount=request.amount,
            payment_gateway=request.payment_gateway
        )
        return {
            "transaction_id": transaction.id,
            "status": transaction.status,
            "amount": transaction.amount,
            "message": "Deposit successful"
        }
    except AppException as e:
        raise to_http_exception(e)


@router.post("/withdraw", status_code=status.HTTP_201_CREATED)
def withdraw_funds(
    user_id: int = Query(...),
    request: WithdrawRequest = None,
    session: Session = Depends(get_db_session)
):
    """Withdraw funds from wallet"""
    try:
        wallet_service = WalletService(session)
        transaction = wallet_service.withdraw_funds(
            user_id=user_id,
            amount=request.amount
        )
        return {
            "transaction_id": transaction.id,
            "status": transaction.status,
            "amount": transaction.amount,
            "message": "Withdrawal successful"
        }
    except AppException as e:
        raise to_http_exception(e)


@router.get("/transactions", response_model=TransactionHistoryResponse)
def get_transactions(
    user_id: int = Query(...),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    session: Session = Depends(get_db_session)
):
    """Get transaction history"""
    try:
        wallet_service = WalletService(session)
        transactions, total = wallet_service.get_transaction_history(
            user_id=user_id,
            offset=offset,
            limit=limit
        )
        return {
            "total": total,
            "page": offset // limit + 1,
            "limit": limit,
            "data": transactions
        }
    except AppException as e:
        raise to_http_exception(e)
