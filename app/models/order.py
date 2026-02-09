from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base


class Order(Base):
    """Order model representing a customer order."""
    
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(255), nullable=False)
    customer_email = Column(String(255), nullable=False)
    total_amount = Column(Float, nullable=False)
    item_details = Column(String(1000), nullable=False)  # JSON string
    status = Column(String(50), default="pending", nullable=False)  # pending, confirmed, delivered
    is_paid = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Order(id={self.id}, customer_name={self.customer_name}, status={self.status})>"
