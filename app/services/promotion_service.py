"""Service for promotion management and calculations."""
from sqlalchemy.orm import Session
from datetime import datetime
from app.repositories.promotion_repository import PromotionRepository
from app.schemas.promotion import PromotionCreate, PromotionUpdate


class PromotionService:
    """Service for managing promotions and applying discounts."""

    def __init__(self, db: Session):
        self.db = db
        self.repo = PromotionRepository()

    def create_promotion(self, promotion_data: PromotionCreate) -> dict:
        """Create a new promotion."""
        # Check if code already exists
        existing = self.repo.get_by_code(self.db, promotion_data.code)
        if existing:
            raise ValueError(f"Promotion code '{promotion_data.code}' already exists")
        
        promotion = self.repo.create(self.db, promotion_data)
        return promotion

    def get_promotion(self, promotion_id: int) -> dict:
        """Get promotion by ID."""
        return self.repo.get_by_id(self.db, promotion_id)

    def get_all_promotions(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> list:
        """Get all promotions."""
        return self.repo.get_all(self.db, skip, limit, active_only)

    def update_promotion(self, promotion_id: int, promotion_data: PromotionUpdate) -> dict:
        """Update a promotion."""
        promotion = self.repo.update(self.db, promotion_id, promotion_data)
        if not promotion:
            raise ValueError(f"Promotion with ID {promotion_id} not found")
        return promotion

    def delete_promotion(self, promotion_id: int) -> bool:
        """Delete a promotion."""
        return self.repo.delete(self.db, promotion_id)

    def apply_promotion(self, code: str, order_total: float) -> dict:
        """Apply a promotion code to an order and return discount details."""
        code_upper = code.upper()
        promotion = self.repo.get_by_code(self.db, code_upper)
        
        if not promotion:
            return {
                "is_valid": False,
                "message": f"Promotion code '{code}' not found",
                "discount_amount": 0,
                "final_total": order_total
            }
        
        # Check if promotion is active
        now = datetime.utcnow()
        if not promotion.is_active:
            return {
                "is_valid": False,
                "message": f"Promotion code '{code}' is inactive",
                "discount_amount": 0,
                "final_total": order_total
            }
        
        # Check if promotion is within valid dates
        if promotion.valid_from > now:
            return {
                "is_valid": False,
                "message": f"Promotion code '{code}' is not yet valid",
                "discount_amount": 0,
                "final_total": order_total
            }
        
        if promotion.valid_until and promotion.valid_until < now:
            return {
                "is_valid": False,
                "message": f"Promotion code '{code}' has expired",
                "discount_amount": 0,
                "final_total": order_total
            }
        
        # Check usage limit
        if promotion.usage_limit and promotion.usage_count >= promotion.usage_limit:
            return {
                "is_valid": False,
                "message": f"Promotion code '{code}' has reached its usage limit",
                "discount_amount": 0,
                "final_total": order_total
            }
        
        # Check minimum order amount
        if order_total < promotion.min_order_amount:
            return {
                "is_valid": False,
                "message": f"Minimum order amount of ${promotion.min_order_amount:.2f} required",
                "discount_amount": 0,
                "final_total": order_total
            }
        
        # Calculate discount
        if promotion.discount_type == "percentage":
            discount_amount = order_total * (promotion.discount_value / 100)
            if promotion.max_discount_amount:
                discount_amount = min(discount_amount, promotion.max_discount_amount)
        else:  # fixed
            discount_amount = min(promotion.discount_value, order_total)
        
        final_total = max(0, order_total - discount_amount)
        
        # Increment promotion usage
        self.repo.increment_usage(self.db, promotion.id)
        
        return {
            "is_valid": True,
            "promotion_id": promotion.id,
            "code": promotion.code,
            "title": promotion.title,
            "discount_type": promotion.discount_type,
            "discount_value": promotion.discount_value,
            "discount_amount": round(discount_amount, 2),
            "final_total": round(final_total, 2),
            "message": f"Promotion applied successfully! Saved ${discount_amount:.2f}"
        }

    def get_active_promotions(self) -> list:
        """Get all currently active promotions."""
        return self.repo.get_valid_promotions(self.db)
