from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class PaymentOrderRequest(BaseModel):
    """Payment order creation request"""
    amount: float = Field(..., gt=0)
    payment_gateway: str  # razorpay, stripe, cashfree
    description: Optional[str] = None


class PaymentVerifyRequest(BaseModel):
    """Payment verification request"""
    order_id: str
    payment_id: str
    signature: str


class PaymentWebhookRequest(BaseModel):
    """Payment webhook request"""
    event: str
    data: dict


class PaymentResponse(BaseModel):
    """Payment response schema"""
    order_id: str
    amount: float
    currency: str = "INR"
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
