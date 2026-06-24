from typing import Optional
from sqlmodel import Session
from app.models.models import Wallet, Transaction
from app.core.exceptions import (
    InsufficientFundsException,
    NotFoundException,
    ValidationException
)
from app.repositories.wallet_repository import (
    WalletRepository,
    TransactionRepository
)
from app.core.constants import TransactionType, TransactionStatus
from datetime import datetime


class WalletService:
    """Wallet service"""
    
    def __init__(self, session: Session):
        self.session = session
        self.wallet_repo = WalletRepository(session)
        self.transaction_repo = TransactionRepository(session)
    
    def get_wallet(self, user_id: int) -> Wallet:
        """Get user wallet"""
        wallet = self.wallet_repo.get_wallet_by_user_id(user_id)
        
        if not wallet:
            raise NotFoundException("Wallet not found")
        
        return wallet
    
    def deposit_funds(
        self,
        user_id: int,
        amount: float,
        payment_gateway: str,
        gateway_reference: Optional[str] = None
    ) -> Transaction:
        """Deposit funds to wallet"""
        if amount <= 0:
            raise ValidationException("Amount must be greater than 0")
        
        wallet = self.wallet_repo.get_wallet_by_user_id(user_id)
        
        if not wallet:
            raise NotFoundException("Wallet not found")
        
        # Create transaction
        transaction = Transaction(
            wallet_id=wallet.id,
            user_id=user_id,
            amount=amount,
            transaction_type=TransactionType.DEPOSIT,
            status=TransactionStatus.COMPLETED,
            gateway_reference=gateway_reference,
            completed_at=datetime.utcnow()
        )
        
        transaction = self.transaction_repo.create_transaction(transaction)
        
        # Update wallet balance
        self.wallet_repo.update_balance(wallet.id, amount)
        
        return transaction
    
    def withdraw_funds(
        self,
        user_id: int,
        amount: float
    ) -> Transaction:
        """Withdraw funds from wallet"""
        if amount <= 0:
            raise ValidationException("Amount must be greater than 0")
        
        wallet = self.wallet_repo.get_wallet_by_user_id(user_id)
        
        if not wallet:
            raise NotFoundException("Wallet not found")
        
        if wallet.balance < amount:
            raise InsufficientFundsException(
                f"Insufficient funds. Available: {wallet.balance}"
            )
        
        # Create transaction
        transaction = Transaction(
            wallet_id=wallet.id,
            user_id=user_id,
            amount=amount,
            transaction_type=TransactionType.WITHDRAWAL,
            status=TransactionStatus.COMPLETED,
            completed_at=datetime.utcnow()
        )
        
        transaction = self.transaction_repo.create_transaction(transaction)
        
        # Update wallet balance
        self.wallet_repo.update_balance(wallet.id, -amount)
        
        return transaction
    
    def lock_funds(
        self,
        user_id: int,
        amount: float
    ) -> bool:
        """Lock funds for bidding"""
        wallet = self.wallet_repo.get_wallet_by_user_id(user_id)
        
        if not wallet:
            raise NotFoundException("Wallet not found")
        
        return self.wallet_repo.lock_amount(wallet.id, amount)
    
    def unlock_funds(
        self,
        user_id: int,
        amount: float
    ) -> bool:
        """Unlock funds"""
        wallet = self.wallet_repo.get_wallet_by_user_id(user_id)
        
        if not wallet:
            raise NotFoundException("Wallet not found")
        
        return self.wallet_repo.unlock_amount(wallet.id, amount)
    
    def get_transaction_history(
        self,
        user_id: int,
        offset: int = 0,
        limit: int = 50
    ) -> tuple[list[Transaction], int]:
        """Get transaction history"""
        wallet = self.wallet_repo.get_wallet_by_user_id(user_id)
        
        if not wallet:
            raise NotFoundException("Wallet not found")
        
        return self.transaction_repo.get_transactions_by_wallet(
            wallet.id,
            offset=offset,
            limit=limit
        )
