import json
from sqlalchemy.orm import Session
from app.repositories import OrderRepository, FoodRepository
from app.schemas import OrderCreate, OrderUpdate
from app.models import Order
from typing import List, Optional


class OrderService:
    """Business logic layer for order operations."""
    
    def __init__(self, db: Session):
        self.order_repository = OrderRepository(db)
        self.food_repository = FoodRepository(db)
    
    def create_order(self, order_data: OrderCreate) -> Optional[Order]:
        """Create a new order with validation and stock management."""
        # Validate all foods exist and have sufficient stock
        item_details = []
        total_amount = 0.0
        
        for item in order_data.items:
            food = self.food_repository.get_by_id(item.food_id)
            if not food:
                raise ValueError(f"Food with ID {item.food_id} not found")
            if food.stock < item.quantity:
                raise ValueError(f"Insufficient stock for {food.name}")
            
            item_details.append({
                "food_id": food.id,
                "food_name": food.name,
                "quantity": item.quantity,
                "unit_price": food.price,
                "subtotal": food.price * item.quantity
            })
            total_amount += food.price * item.quantity
        
        # Create order
        order_dict = {
            "customer_name": order_data.customer_name,
            "customer_email": order_data.customer_email,
            "total_amount": total_amount,
            "item_details": json.dumps(item_details),
            "status": "pending",
            "is_paid": False
        }
        
        order = self.order_repository.create(order_dict)
        
        # Reduce stock for each item
        for item in order_data.items:
            self.food_repository.decrease_stock(item.food_id, item.quantity)
        
        return order
    
    def get_order(self, order_id: int) -> Optional[Order]:
        """Get an order by ID."""
        return self.order_repository.get_by_id(order_id)
    
    def get_all_orders(self, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get all orders."""
        return self.order_repository.get_all(skip, limit)
    
    def get_orders_by_customer(self, email: str, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get orders by customer email."""
        return self.order_repository.get_by_customer_email(email, skip, limit)
    
    def get_orders_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Order]:
        """Get orders by status."""
        return self.order_repository.get_by_status(status, skip, limit)
    
    def update_order(self, order_id: int, order_data: OrderUpdate) -> Optional[Order]:
        """Update an order."""
        order_dict = order_data.model_dump(exclude_unset=True)
        return self.order_repository.update(order_id, order_dict)
    
    def confirm_order(self, order_id: int) -> Optional[Order]:
        """Confirm an order."""
        return self.order_repository.update(order_id, {"status": "confirmed"})
    
    def mark_as_delivered(self, order_id: int) -> Optional[Order]:
        """Mark an order as delivered."""
        return self.order_repository.update(order_id, {"status": "delivered"})
    
    def mark_as_paid(self, order_id: int) -> Optional[Order]:
        """Mark an order as paid."""
        return self.order_repository.update(order_id, {"is_paid": True})
    
    def delete_order(self, order_id: int) -> bool:
        """Delete an order."""
        return self.order_repository.delete(order_id)
