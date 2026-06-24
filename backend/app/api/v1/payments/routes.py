from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.schemas.payment import (
    PaymentOrderRequest,
    PaymentVerifyRequest,
    PaymentResponse
)
from app.services.payment_service import PaymentService
from app.db.session import get_db_session
from app.core.exceptions import AppException, to_http_exception

router = APIRouter(prefix="/api/v1/payment", tags=["payment"])


@router.post("/create-order", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_payment_order(
    user_id: int,
    request: PaymentOrderRequest,
    session: Session = Depends(get_db_session)
):
    """Create payment order"""
    try:
        payment_service = PaymentService(session)
        
        if request.payment_gateway == "razorpay":
            order = payment_service.create_razorpay_order(
                user_id=user_id,
                amount=request.amount,
                description=request.description or "CricAuction Deposit"
            )
            return order
        
        raise AppException("Payment gateway not supported")
    
    except AppException as e:
        raise to_http_exception(e)


@router.post("/verify", response_model=dict)
def verify_payment(
    request: PaymentVerifyRequest,
    session: Session = Depends(get_db_session)
):
    """Verify payment"""
    try:
        payment_service = PaymentService(session)
        is_valid = payment_service.verify_razorpay_payment(
            order_id=request.order_id,
            payment_id=request.payment_id,
            signature=request.signature
        )
        
        return {"verified": is_valid, "message": "Payment verified successfully"}
    
    except AppException as e:
        raise to_http_exception(e)


@router.post("/webhook", status_code=status.HTTP_200_OK)
def handle_payment_webhook(
    event_type: str,
    data: dict,
    session: Session = Depends(get_db_session)
):
    """Handle payment webhook"""
    try:
        payment_service = PaymentService(session)
        payment_service.handle_payment_webhook(event_type, data)
        return {"status": "received"}
    
    except AppException as e:
        raise to_http_exception(e)
