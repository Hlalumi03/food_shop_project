"""Routes for promotion management."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.promotion_service import PromotionService
from app.schemas.promotion import (
    PromotionCreate, PromotionUpdate, PromotionResponse,
    ApplyPromotion, PromotionResult
)
from typing import List

router = APIRouter()


@router.post("", response_model=PromotionResponse, status_code=201)
def create_promotion(
    promotion_data: PromotionCreate,
    db: Session = Depends(get_db)
):
    """Create a new promotion."""
    try:
        service = PromotionService(db)
        promotion = service.create_promotion(promotion_data)
        return promotion
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{promotion_id}", response_model=PromotionResponse)
def get_promotion(
    promotion_id: int,
    db: Session = Depends(get_db)
):
    """Get a promotion by ID."""
    service = PromotionService(db)
    promotion = service.get_promotion(promotion_id)
    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")
    return promotion


@router.get("", response_model=List[PromotionResponse])
def get_all_promotions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    """Get all promotions with optional filtering."""
    service = PromotionService(db)
    promotions = service.get_all_promotions(skip, limit, active_only)
    return promotions


@router.put("/{promotion_id}", response_model=PromotionResponse)
def update_promotion(
    promotion_id: int,
    promotion_data: PromotionUpdate,
    db: Session = Depends(get_db)
):
    """Update a promotion."""
    try:
        service = PromotionService(db)
        promotion = service.update_promotion(promotion_id, promotion_data)
        return promotion
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{promotion_id}", status_code=204)
def delete_promotion(
    promotion_id: int,
    db: Session = Depends(get_db)
):
    """Delete a promotion."""
    service = PromotionService(db)
    success = service.delete_promotion(promotion_id)
    if not success:
        raise HTTPException(status_code=404, detail="Promotion not found")


@router.post("/apply", response_model=PromotionResult)
def apply_promotion(
    apply_data: ApplyPromotion,
    db: Session = Depends(get_db)
):
    """Apply a promotion code to an order."""
    service = PromotionService(db)
    result = service.apply_promotion(apply_data.code, apply_data.order_total)
    return result


@router.get("/active/all", response_model=List[PromotionResponse])
def get_active_promotions(
    db: Session = Depends(get_db)
):
    """Get all currently active promotions."""
    service = PromotionService(db)
    promotions = service.get_active_promotions()
    return promotions
