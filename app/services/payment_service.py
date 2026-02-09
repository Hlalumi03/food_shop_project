import uuid
from sqlalchemy.orm import Session
from app.repositories import PaymentRepository, OrderRepository
from app.schemas import PaymentCreate, PaymentUpdate
from app.models.payment import Payment, PaymentStatusEnum, PaymentMethodEnum
from typing import List, Optional


class PaymentService:
    """Business logic layer for payment operations."""
    
    def __init__(self, db: Session):
        self.repository = PaymentRepository(db)
        self.order_repository = OrderRepository(db)
    
    def validate_payment_method(self, method: str) -> bool:
        """Validate if payment method is supported."""
        valid_methods = [pm.value for pm in PaymentMethodEnum]
        return method in valid_methods
    
    def validate_order_exists(self, order_id: int) -> bool:
        """Validate if order exists."""
        return self.order_repository.get_by_id(order_id) is not None
    
    def generate_reference_number(self) -> str:
        """Generate a unique reference number."""
        return f"PAY-{uuid.uuid4().hex[:12].upper()}"
    
    def create_payment(self, payment_data: PaymentCreate) -> Payment:
        """Create a new payment with validation."""
        # Validate order exists
        order = self.order_repository.get_by_id(payment_data.order_id)
        if not order:
            raise ValueError(f"Order with ID {payment_data.order_id} not found")
        
        # Validate payment method
        if not self.validate_payment_method(payment_data.payment_method):
            raise ValueError(f"Invalid payment method: {payment_data.payment_method}")
        
        # Validate amount matches order total
        if payment_data.amount != order.total_amount:
            raise ValueError(
                f"Payment amount {payment_data.amount} does not match order total {order.total_amount}"
            )
        
        # Create payment
        payment_dict = {
            "order_id": payment_data.order_id,
            "payment_method": payment_data.payment_method,
            "amount": payment_data.amount,
            "status": PaymentStatusEnum.PENDING,
            "card_last_four": payment_data.card_last_four,
            "notes": payment_data.notes,
            "reference_number": self.generate_reference_number()
        }
        
        return self.repository.create(payment_dict)
    
    def get_payment(self, payment_id: int) -> Optional[Payment]:
        """Get a payment by ID."""
        return self.repository.get_by_id(payment_id)
    
    def get_all_payments(self, skip: int = 0, limit: int = 100) -> List[Payment]:
        """Get all payments."""
        return self.repository.get_all(skip, limit)
    
    def get_payments_by_order(self, order_id: int) -> List[Payment]:
        """Get all payments for an order."""
        return self.repository.get_by_order_id(order_id)
    
    def get_payments_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[Payment]:
        """Get payments by status."""
        return self.repository.get_by_status(status, skip, limit)
    
    def get_payments_by_method(self, method: str, skip: int = 0, limit: int = 100) -> List[Payment]:
        """Get payments by payment method."""
        return self.repository.get_by_method(method, skip, limit)
    
    def update_payment(self, payment_id: int, payment_data: PaymentUpdate) -> Optional[Payment]:
        """Update a payment."""
        payment = self.repository.get_by_id(payment_id)
        if not payment:
            return None
        
        payment_dict = payment_data.model_dump(exclude_unset=True)
        return self.repository.update(payment_id, payment_dict)
    
    def confirm_payment(self, payment_id: int, transaction_id: str) -> Optional[Payment]:
        """Confirm a payment and mark as completed."""
        payment = self.repository.get_by_id(payment_id)
        if not payment:
            return None
        
        if payment.status != PaymentStatusEnum.PENDING:
            raise ValueError(f"Cannot confirm payment with status: {payment.status}")
        
        # Mark payment as completed
        payment = self.repository.mark_as_completed(payment_id, transaction_id)
        
        # Mark order as paid
        if payment:
            self.order_repository.update(payment.order_id, {"is_paid": True})
        
        return payment
    
    def fail_payment(self, payment_id: int, reason: str = None) -> Optional[Payment]:
        """Mark a payment as failed."""
        payment = self.repository.get_by_id(payment_id)
        if not payment:
            return None
        
        return self.repository.mark_as_failed(payment_id, reason)
    
    def refund_payment(self, payment_id: int) -> Optional[Payment]:
        """Refund a completed payment."""
        payment = self.repository.get_by_id(payment_id)
        if not payment:
            return None
        
        if payment.status != PaymentStatusEnum.COMPLETED:
            raise ValueError(f"Can only refund completed payments. Current status: {payment.status}")
        
        # Mark payment as refunded
        refunded_payment = self.repository.refund_payment(payment_id)
        
        # Mark order as not paid
        if refunded_payment:
            self.order_repository.update(payment.order_id, {"is_paid": False})
        
        return refunded_payment
    
    def delete_payment(self, payment_id: int) -> bool:
        """Delete a payment."""
        return self.repository.delete(payment_id)
    
    def get_payment_statistics(self) -> dict:
        """Get payment statistics."""
        all_payments = self.repository.get_all(skip=0, limit=999999)
        
        total_amount = sum(p.amount for p in all_payments)
        completed_amount = sum(
            p.amount for p in all_payments 
            if p.status == PaymentStatusEnum.COMPLETED
        )
        
        return {
            "total_payments": len(all_payments),
            "total_amount": total_amount,
            "completed_amount": completed_amount,
            "pending_amount": sum(
                p.amount for p in all_payments 
                if p.status == PaymentStatusEnum.PENDING
            ),
            "completed_count": len([p for p in all_payments if p.status == PaymentStatusEnum.COMPLETED]),
            "pending_count": len([p for p in all_payments if p.status == PaymentStatusEnum.PENDING]),
            "failed_count": len([p for p in all_payments if p.status == PaymentStatusEnum.FAILED]),
            "refunded_count": len([p for p in all_payments if p.status == PaymentStatusEnum.REFUNDED]),
        }
