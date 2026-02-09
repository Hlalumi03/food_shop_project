from sqlalchemy.orm import Session
from app.models import Order
from typing import List, Optional


class OrderRepository:
    """Repository pattern for Order model - handles database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, order_data: dict) -> Order:
        """Create a new order."""
        order = Order(**order_data)
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def get_by_id(self, order_id: int) -> Optional[Order]:
        """Get an order by ID."""
        return self.db.query(Order).filter(Order.id == order_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get all orders with pagination."""
        return self.db.query(Order).offset(skip).limit(limit).all()
    
    def get_by_customer_email(self, email: str, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get orders by customer email."""
        return self.db.query(Order).filter(Order.customer_email == email).offset(skip).limit(limit).all()
    
    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get orders by status."""
        return self.db.query(Order).filter(Order.status == status).offset(skip).limit(limit).all()
    
    def update(self, order_id: int, order_data: dict) -> Optional[Order]:
        """Update an order."""
        order = self.get_by_id(order_id)
        if not order:
            return None
        
        for key, value in order_data.items():
            if value is not None:
                setattr(order, key, value)
        
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def delete(self, order_id: int) -> bool:
        """Delete an order."""
        order = self.get_by_id(order_id)
        if not order:
            return False
        
        self.db.delete(order)
        self.db.commit()
        return True
