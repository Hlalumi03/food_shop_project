from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PaymentCreate(BaseModel):
    """DTO for creating a payment."""
    
    order_id: int = Field(..., gt=0)
    payment_method: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    card_last_four: Optional[str] = Field(None, min_length=4, max_length=4)
    notes: Optional[str] = Field(None, max_length=500)


class PaymentUpdate(BaseModel):
    """DTO for updating a payment."""
    
    status: Optional[str] = None
    transaction_id: Optional[str] = Field(None, min_length=1, max_length=255)
    reference_number: Optional[str] = Field(None, min_length=1, max_length=255)
    notes: Optional[str] = Field(None, max_length=500)


class PaymentResponse(BaseModel):
    """DTO for payment response."""
    
    id: int
    order_id: int
    payment_method: str
    amount: float
    status: str
    transaction_id: Optional[str]
    reference_number: Optional[str]
    card_last_four: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PaymentConfirm(BaseModel):
    """DTO for confirming a payment."""
    
    transaction_id: str = Field(..., min_length=1, max_length=255)
    reference_number: Optional[str] = Field(None, min_length=1, max_length=255)


class PaymentRefund(BaseModel):
    """DTO for refunding a payment."""
    
    reason: Optional[str] = Field(None, max_length=500)
