from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class WalletResponse(BaseModel):
    """Wallet response schema"""
    id: int
    user_id: int
    balance: float
    locked_balance: float
    available_balance: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DepositRequest(BaseModel):
    """Deposit request schema"""
    amount: float = Field(..., gt=0)
    payment_gateway: str  # razorpay, stripe, cashfree


class WithdrawRequest(BaseModel):
    """Withdraw request schema"""
    amount: float = Field(..., gt=0)
    bank_account_id: Optional[int] = None


class TransactionResponse(BaseModel):
    """Transaction response schema"""
    id: int
    user_id: int
    amount: float
    transaction_type: str
    status: str
    gateway_reference: Optional[str]
    description: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class TransactionHistoryResponse(BaseModel):
    """Transaction history response schema"""
    total: int
    page: int
    limit: int
    data: list[TransactionResponse]
