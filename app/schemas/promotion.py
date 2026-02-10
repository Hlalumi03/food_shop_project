"""Schemas for promotion requests and responses."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PromotionCreate(BaseModel):
    """DTO for creating a promotion."""
    code: str = Field(..., min_length=1, max_length=50)
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    discount_type: str = Field(..., pattern="^(percentage|fixed)$")
    discount_value: float = Field(..., gt=0)
    min_order_amount: float = Field(default=0, ge=0)
    max_discount_amount: Optional[float] = Field(None, gt=0)
    applicable_categories: Optional[str] = None
    is_active: bool = Field(default=True)
    usage_limit: Optional[int] = Field(None, ge=1)
    valid_until: Optional[datetime] = None


class PromotionUpdate(BaseModel):
    """DTO for updating a promotion."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None
    discount_value: Optional[float] = Field(None, gt=0)
    min_order_amount: Optional[float] = Field(None, ge=0)
    usage_limit: Optional[int] = Field(None, ge=1)
    valid_until: Optional[datetime] = None


class PromotionResponse(BaseModel):
    """DTO for promotion response."""
    id: int
    code: str
    title: str
    description: Optional[str]
    discount_type: str
    discount_value: float
    min_order_amount: float
    max_discount_amount: Optional[float]
    applicable_categories: Optional[str]
    is_active: bool
    usage_limit: Optional[int]
    usage_count: int
    valid_from: datetime
    valid_until: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ApplyPromotion(BaseModel):
    """DTO for applying a promotion code."""
    code: str = Field(..., min_length=1, max_length=50)
    order_total: float = Field(..., gt=0)


class PromotionResult(BaseModel):
    """DTO for promotion application result."""
    promotion_id: int
    code: str
    title: str
    discount_type: str
    discount_value: float
    discount_amount: float
    final_total: float
    is_valid: bool
    message: str
