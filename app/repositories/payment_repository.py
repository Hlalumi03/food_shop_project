from sqlalchemy.orm import Session
from app.models.payment import Payment, PaymentStatusEnum
from typing import List, Optional


class PaymentRepository:
    """Repository pattern for Payment model - handles database operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, payment_data: dict) -> Payment:
        """Create a new payment."""
        payment = Payment(**payment_data)
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment
    
    def get_by_id(self, payment_id: int) -> Optional[Payment]:
        """Get a payment by ID."""
        return self.db.query(Payment).filter(Payment.id == payment_id).first()
    
    def get_by_transaction_id(self, transaction_id: str) -> Optional[Payment]:
        """Get a payment by transaction ID."""
        return self.db.query(Payment).filter(Payment.transaction_id == transaction_id).first()
    
    def get_by_order_id(self, order_id: int) -> List[Payment]:
        """Get all payments for an order."""
        return self.db.query(Payment).filter(Payment.order_id == order_id).all()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Payment]:
        """Get all payments with pagination."""
        return self.db.query(Payment).offset(skip).limit(limit).all()
    
    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Payment]:
        """Get payments by status."""
        return self.db.query(Payment).filter(Payment.status == status).offset(skip).limit(limit).all()
    
    def get_by_method(self, method: str, skip: int = 0, limit: int = 100) -> List[Payment]:
        """Get payments by payment method."""
        return self.db.query(Payment).filter(Payment.payment_method == method).offset(skip).limit(limit).all()
    
    def update(self, payment_id: int, payment_data: dict) -> Optional[Payment]:
        """Update a payment."""
        payment = self.get_by_id(payment_id)
        if not payment:
            return None
        
        for key, value in payment_data.items():
            if value is not None:
                setattr(payment, key, value)
        
        self.db.commit()
        self.db.refresh(payment)
        return payment
    
    def delete(self, payment_id: int) -> bool:
        """Delete a payment."""
        payment = self.get_by_id(payment_id)
        if not payment:
            return False
        
        self.db.delete(payment)
        self.db.commit()
        return True
    
    def mark_as_completed(self, payment_id: int, transaction_id: str) -> Optional[Payment]:
        """Mark a payment as completed."""
        return self.update(payment_id, {
            "status": PaymentStatusEnum.COMPLETED,
            "transaction_id": transaction_id
        })
    
    def mark_as_failed(self, payment_id: int, notes: str = None) -> Optional[Payment]:
        """Mark a payment as failed."""
        return self.update(payment_id, {
            "status": PaymentStatusEnum.FAILED,
            "notes": notes
        })
    
    def refund_payment(self, payment_id: int) -> Optional[Payment]:
        """Mark a payment as refunded."""
        return self.update(payment_id, {"status": PaymentStatusEnum.REFUNDED})
