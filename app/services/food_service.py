from sqlalchemy.orm import Session
from app.repositories import FoodRepository
from app.schemas import FoodCreate, FoodUpdate
from app.models import Food
from typing import List, Optional


class FoodService:
    """Business logic layer for food operations."""
    
    def __init__(self, db: Session):
        self.repository = FoodRepository(db)
    
    def create_food(self, food_data: FoodCreate) -> Food:
        """Create a new food item."""
        food_dict = food_data.model_dump()
        return self.repository.create(food_dict)
    
    def get_food(self, food_id: int) -> Optional[Food]:
        """Get a food item by ID."""
        return self.repository.get_by_id(food_id)
    
    def get_all_foods(self, skip: int = 0, limit: int = 100) -> List[Food]:
        """Get all food items."""
        return self.repository.get_all(skip, limit)
    
    def get_foods_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[Food]:
        """Get food items by category."""
        return self.repository.get_by_category(category, skip, limit)
    
    def update_food(self, food_id: int, food_data: FoodUpdate) -> Optional[Food]:
        """Update a food item."""
        food_dict = food_data.model_dump(exclude_unset=True)
        return self.repository.update(food_id, food_dict)
    
    def delete_food(self, food_id: int) -> bool:
        """Delete a food item."""
        return self.repository.delete(food_id)
    
    def check_stock(self, food_id: int, quantity: int) -> bool:
        """Check if sufficient stock is available."""
        food = self.repository.get_by_id(food_id)
        return food is not None and food.stock >= quantity
    
    def reduce_stock(self, food_id: int, quantity: int) -> bool:
        """Reduce stock for a food item."""
        result = self.repository.decrease_stock(food_id, quantity)
        return result is not None
