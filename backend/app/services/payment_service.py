from typing import Optional
from sqlmodel import Session
from app.models.models import Transaction
from app.core.exceptions import PaymentException, NotFoundException
from app.repositories.wallet_repository import TransactionRepository
from app.core.constants import TransactionStatus


class PaymentService:
    """Payment service"""
    
    def __init__(self, session: Session):
        self.session = session
        self.transaction_repo = TransactionRepository(session)
    
    def create_razorpay_order(
        self,
        user_id: int,
        amount: float,
        description: str
    ) -> dict:
        """Create Razorpay payment order"""
        try:
            import razorpay
            from app.core.config import get_settings
            
            settings = get_settings()
            
            client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )
            
            order_data = {
                "amount": int(amount * 100),  # Amount in paise
                "currency": "INR",
                "receipt": f"user_{user_id}",
                "notes": {
                    "user_id": str(user_id),
                    "description": description
                }
            }
            
            order = client.order.create(data=order_data)
            
            return {
                "order_id": order["id"],
                "amount": amount,
                "currency": "INR"
            }
        
        except Exception as e:
            raise PaymentException(f"Failed to create payment order: {str(e)}")
    
    def verify_razorpay_payment(
        self,
        order_id: str,
        payment_id: str,
        signature: str
    ) -> bool:
        """Verify Razorpay payment"""
        try:
            import razorpay
            from app.core.config import get_settings
            
            settings = get_settings()
            
            client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )
            
            params_dict = {
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature
            }
            
            client.utility.verify_payment_signature(params_dict)
            return True
        
        except Exception as e:
            raise PaymentException(f"Payment verification failed: {str(e)}")
    
    def handle_payment_webhook(
        self,
        event_type: str,
        data: dict
    ) -> None:
        """Handle payment webhook"""
        if event_type == "payment.authorized":
            payment_id = data.get("payment", {}).get("id")
            # Update transaction status
            transaction = self.transaction_repo.get_transactions_by_gateway_reference(
                payment_id
            )
            if transaction:
                self.transaction_repo.update_transaction(
                    transaction.id,
                    status=TransactionStatus.COMPLETED
                )
        
        elif event_type == "payment.failed":
            payment_id = data.get("payment", {}).get("id")
            # Update transaction status
            transaction = self.transaction_repo.get_transactions_by_gateway_reference(
                payment_id
            )
            if transaction:
                self.transaction_repo.update_transaction(
                    transaction.id,
                    status=TransactionStatus.FAILED
                )
