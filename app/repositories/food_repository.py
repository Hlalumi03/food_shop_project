from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models import Food
from typing import List, Optional


class FoodRepository:
    """Repository pattern for Food model - handles database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, food_data: dict) -> Food:
        """Create a new food item."""
        food = Food(**food_data)
        self.db.add(food)
        self.db.commit()
        self.db.refresh(food)
        return food
    
    def get_by_id(self, food_id: int) -> Optional[Food]:
        """Get a food item by ID."""
        return self.db.query(Food).filter(Food.id == food_id).first()
    
    def get_by_name(self, name: str) -> Optional[Food]:
        """Get a food item by name."""
        return self.db.query(Food).filter(Food.name == name).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Food]:
        """Get all food items with pagination."""
        return self.db.query(Food).offset(skip).limit(limit).all()
    
    def get_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[Food]:
        """Get food items by category."""
        return self.db.query(Food).filter(Food.category == category).offset(skip).limit(limit).all()
    
    def update(self, food_id: int, food_data: dict) -> Optional[Food]:
        """Update a food item."""
        food = self.get_by_id(food_id)
        if not food:
            return None
        
        for key, value in food_data.items():
            if value is not None:
                setattr(food, key, value)
        
        self.db.commit()
        self.db.refresh(food)
        return food
    
    def delete(self, food_id: int) -> bool:
        """Delete a food item."""
        food = self.get_by_id(food_id)
        if not food:
            return False
        
        self.db.delete(food)
        self.db.commit()
        return True
    
    def decrease_stock(self, food_id: int, quantity: int) -> Optional[Food]:
        """Decrease stock of a food item."""
        food = self.get_by_id(food_id)
        if not food or food.stock < quantity:
            return None
        
        food.stock -= quantity
        self.db.commit()
        self.db.refresh(food)
        return food
