from typing import Optional, List
from sqlmodel import Session, select
from app.models.models import Wallet, Transaction
from app.core.constants import TransactionStatus


class WalletRepository:
    """Wallet repository for database operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_wallet_by_user_id(self, user_id: int) -> Optional[Wallet]:
        """Get wallet by user ID"""
        statement = select(Wallet).where(Wallet.user_id == user_id)
        return self.session.exec(statement).first()
    
    def create_wallet(self, wallet: Wallet) -> Wallet:
        """Create a new wallet"""
        self.session.add(wallet)
        self.session.commit()
        self.session.refresh(wallet)
        return wallet
    
    def update_balance(self, wallet_id: int, amount: float) -> Optional[Wallet]:
        """Update wallet balance"""
        wallet = self.session.get(Wallet, wallet_id)
        if wallet:
            wallet.balance += amount
            self.session.add(wallet)
            self.session.commit()
            self.session.refresh(wallet)
        return wallet
    
    def lock_amount(self, wallet_id: int, amount: float) -> bool:
        """Lock amount in wallet"""
        wallet = self.session.get(Wallet, wallet_id)
        if wallet and wallet.balance >= amount:
            wallet.balance -= amount
            wallet.locked_balance += amount
            self.session.add(wallet)
            self.session.commit()
            return True
        return False
    
    def unlock_amount(self, wallet_id: int, amount: float) -> bool:
        """Unlock amount in wallet"""
        wallet = self.session.get(Wallet, wallet_id)
        if wallet and wallet.locked_balance >= amount:
            wallet.locked_balance -= amount
            wallet.balance += amount
            self.session.add(wallet)
            self.session.commit()
            return True
        return False
    
    def deduct_locked_amount(self, wallet_id: int, amount: float) -> bool:
        """Deduct locked amount from wallet (finalize transaction)"""
        wallet = self.session.get(Wallet, wallet_id)
        if wallet and wallet.locked_balance >= amount:
            wallet.locked_balance -= amount
            self.session.add(wallet)
            self.session.commit()
            return True
        return False
    
    def get_available_balance(self, wallet_id: int) -> float:
        """Get available balance"""
        wallet = self.session.get(Wallet, wallet_id)
        if wallet:
            return wallet.balance
        return 0.0


class TransactionRepository:
    """Transaction repository for database operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_transaction(self, transaction: Transaction) -> Transaction:
        """Create a new transaction"""
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        return transaction
    
    def get_transaction_by_id(self, transaction_id: int) -> Optional[Transaction]:
        """Get transaction by ID"""
        return self.session.get(Transaction, transaction_id)
    
    def get_transactions_by_wallet(
        self,
        wallet_id: int,
        offset: int = 0,
        limit: int = 50
    ) -> tuple[List[Transaction], int]:
        """Get all transactions for a wallet"""
        query = select(Transaction).where(Transaction.wallet_id == wallet_id)
        total = len(self.session.exec(query).all())
        
        query = query.order_by(Transaction.created_at.desc()).offset(offset).limit(limit)
        transactions = self.session.exec(query).all()
        
        return transactions, total
    
    def update_transaction(
        self,
        transaction_id: int,
        **kwargs
    ) -> Optional[Transaction]:
        """Update transaction"""
        transaction = self.get_transaction_by_id(transaction_id)
        if transaction:
            for key, value in kwargs.items():
                if hasattr(transaction, key) and value is not None:
                    setattr(transaction, key, value)
            self.session.add(transaction)
            self.session.commit()
            self.session.refresh(transaction)
        return transaction
    
    def get_transactions_by_gateway_reference(
        self,
        gateway_reference: str
    ) -> Optional[Transaction]:
        """Get transaction by gateway reference"""
        query = select(Transaction).where(
            Transaction.gateway_reference == gateway_reference
        )
        return self.session.exec(query).first()
