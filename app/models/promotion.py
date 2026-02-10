"""Promotion model for discounts and special offers."""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from datetime import datetime
from app.core.database import Base


class Promotion(Base):
    """Model for promotional discounts and special offers."""
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    discount_type = Column(String(20), nullable=False)  # "percentage" or "fixed"
    discount_value = Column(Float, nullable=False)  # percentage (0-100) or fixed amount
    min_order_amount = Column(Float, default=0)  # Minimum order amount to apply
    max_discount_amount = Column(Float, nullable=True)  # Cap on discount (for percentage)
    applicable_categories = Column(String(500), nullable=True)  # Comma-separated categories
    is_active = Column(Boolean, default=True, index=True)
    usage_limit = Column(Integer, nullable=True)  # Total times promotion can be used
    usage_count = Column(Integer, default=0)  # Current usage count
    valid_from = Column(DateTime, default=datetime.utcnow)
    valid_until = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Promotion(id={self.id}, code={self.code}, title={self.title})"
