from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import FoodService
from app.schemas import FoodCreate, FoodUpdate, FoodResponse
from typing import List

router = APIRouter()


@router.post("", response_model=FoodResponse, status_code=201)
def create_food(
    food_data: FoodCreate,
    db: Session = Depends(get_db)
):
    """Create a new food item."""
    try:
        service = FoodService(db)
        food = service.create_food(food_data)
        return food
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{food_id}", response_model=FoodResponse)
def get_food(
    food_id: int,
    db: Session = Depends(get_db)
):
    """Get a food item by ID."""
    service = FoodService(db)
    food = service.get_food(food_id)
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    return food


@router.get("", response_model=List[FoodResponse])
def get_all_foods(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: str = None,
    db: Session = Depends(get_db)
):
    """Get all food items or filter by category."""
    service = FoodService(db)
    
    if category:
        foods = service.get_foods_by_category(category, skip, limit)
    else:
        foods = service.get_all_foods(skip, limit)
    
    return foods


@router.put("/{food_id}", response_model=FoodResponse)
def update_food(
    food_id: int,
    food_data: FoodUpdate,
    db: Session = Depends(get_db)
):
    """Update a food item."""
    service = FoodService(db)
    food = service.update_food(food_id, food_data)
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    return food


@router.delete("/{food_id}", status_code=204)
def delete_food(
    food_id: int,
    db: Session = Depends(get_db)
):
    """Delete a food item."""
    service = FoodService(db)
    success = service.delete_food(food_id)
    if not success:
        raise HTTPException(status_code=404, detail="Food not found")
