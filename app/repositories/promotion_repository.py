"""Repository for promotion database operations."""
from sqlalchemy.orm import Session
from app.models.promotion import Promotion
from app.schemas.promotion import PromotionCreate, PromotionUpdate
from datetime import datetime


class PromotionRepository:
    """Repository for managing promotions in the database."""

    @staticmethod
    def create(db: Session, promotion_data: PromotionCreate) -> Promotion:
        """Create a new promotion."""
        promotion = Promotion(
            code=promotion_data.code.upper(),
            title=promotion_data.title,
            description=promotion_data.description,
            discount_type=promotion_data.discount_type,
            discount_value=promotion_data.discount_value,
            min_order_amount=promotion_data.min_order_amount,
            max_discount_amount=promotion_data.max_discount_amount,
            applicable_categories=promotion_data.applicable_categories,
            is_active=promotion_data.is_active,
            usage_limit=promotion_data.usage_limit,
            valid_until=promotion_data.valid_until
        )
        db.add(promotion)
        db.commit()
        db.refresh(promotion)
        return promotion

    @staticmethod
    def get_by_id(db: Session, promotion_id: int) -> Promotion:
        """Get promotion by ID."""
        return db.query(Promotion).filter(Promotion.id == promotion_id).first()

    @staticmethod
    def get_by_code(db: Session, code: str) -> Promotion:
        """Get promotion by code."""
        return db.query(Promotion).filter(Promotion.code == code.upper()).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, active_only: bool = False) -> list:
        """Get all promotions."""
        query = db.query(Promotion)
        
        if active_only:
            now = datetime.utcnow()
            query = query.filter(
                Promotion.is_active == True,
                Promotion.valid_from <= now
            )
            query = query.filter(
                (Promotion.valid_until == None) | (Promotion.valid_until >= now)
            )
        
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, promotion_id: int, promotion_data: PromotionUpdate) -> Promotion:
        """Update a promotion."""
        promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
        if not promotion:
            return None
        
        update_data = promotion_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(promotion, field, value)
        
        db.commit()
        db.refresh(promotion)
        return promotion

    @staticmethod
    def delete(db: Session, promotion_id: int) -> bool:
        """Delete a promotion."""
        promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
        if not promotion:
            return False
        
        db.delete(promotion)
        db.commit()
        return True

    @staticmethod
    def increment_usage(db: Session, promotion_id: int) -> bool:
        """Increment usage count for a promotion."""
        promotion = db.query(Promotion).filter(Promotion.id == promotion_id).first()
        if not promotion:
            return False
        
        promotion.usage_count += 1
        db.commit()
        return True

    @staticmethod
    def get_valid_promotions(db: Session) -> list:
        """Get all currently valid active promotions."""
        now = datetime.utcnow()
        return db.query(Promotion).filter(
            Promotion.is_active == True,
            Promotion.valid_from <= now,
            (Promotion.valid_until == None) | (Promotion.valid_until >= now)
        ).all()
