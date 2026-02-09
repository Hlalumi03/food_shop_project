from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


class OrderItemIn(BaseModel):
    """DTO for order item input."""
    
    food_id: int
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    """DTO for creating a new order."""
    
    customer_name: str = Field(..., min_length=1, max_length=255)
    customer_email: EmailStr
    items: List[OrderItemIn]


class OrderUpdate(BaseModel):
    """DTO for updating an order."""
    
    status: Optional[str] = Field(None, pattern="^(pending|confirmed|delivered)$")
    is_paid: Optional[bool] = None


class OrderResponse(BaseModel):
    """DTO for order response."""
    
    id: int
    customer_name: str
    customer_email: str
    total_amount: float
    item_details: str
    status: str
    is_paid: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
