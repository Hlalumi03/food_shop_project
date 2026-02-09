from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FoodCreate(BaseModel):
    """DTO for creating a new food item."""
    
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=100)
    stock: int = Field(default=0, ge=0)


class FoodUpdate(BaseModel):
    """DTO for updating a food item."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    stock: Optional[int] = Field(None, ge=0)


class FoodResponse(BaseModel):
    """DTO for food item response."""
    
    id: int
    name: str
    description: Optional[str]
    price: float
    category: str
    stock: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
