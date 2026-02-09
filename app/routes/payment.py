from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import PaymentService
from app.schemas import PaymentCreate, PaymentUpdate, PaymentResponse, PaymentConfirm, PaymentRefund
from typing import List

router = APIRouter()


@router.post("", response_model=PaymentResponse, status_code=201)
def create_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db)
):
    """Create a new payment for an order."""
    try:
        service = PaymentService(db)
        payment = service.create_payment(payment_data)
        return payment
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):
    """Get a payment by ID."""
    service = PaymentService(db)
    payment = service.get_payment(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.get("", response_model=List[PaymentResponse])
def get_all_payments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    order_id: int = None,
    status: str = None,
    method: str = None,
    db: Session = Depends(get_db)
):
    """Get all payments with filters."""
    service = PaymentService(db)
    
    if order_id:
        payments = service.get_payments_by_order(order_id)
    elif status:
        valid_statuses = ["pending", "processing", "completed", "failed", "refunded"]
        if status not in valid_statuses:
            raise HTTPException(status_code=400, detail="Invalid status")
        payments = service.get_payments_by_status(status, skip, limit)
    elif method:
        valid_methods = [
            "credit_card", "debit_card", "paypal", 
            "apple_pay", "google_pay", "bank_transfer", "cash"
        ]
        if method not in valid_methods:
            raise HTTPException(status_code=400, detail="Invalid payment method")
        payments = service.get_payments_by_method(method, skip, limit)
    else:
        payments = service.get_all_payments(skip, limit)
    
    return payments


@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(
    payment_id: int,
    payment_data: PaymentUpdate,
    db: Session = Depends(get_db)
):
    """Update a payment."""
    service = PaymentService(db)
    payment = service.update_payment(payment_id, payment_data)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.post("/{payment_id}/confirm", response_model=PaymentResponse)
def confirm_payment(
    payment_id: int,
    confirm_data: PaymentConfirm,
    db: Session = Depends(get_db)
):
    """Confirm a payment (mark as completed)."""
    try:
        service = PaymentService(db)
        payment = service.confirm_payment(payment_id, confirm_data.transaction_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return payment
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{payment_id}/fail", response_model=PaymentResponse)
def fail_payment(
    payment_id: int,
    reason: str = Query(None),
    db: Session = Depends(get_db)
):
    """Mark a payment as failed."""
    service = PaymentService(db)
    payment = service.fail_payment(payment_id, reason)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.post("/{payment_id}/refund", response_model=PaymentResponse)
def refund_payment(
    payment_id: int,
    refund_data: PaymentRefund = None,
    db: Session = Depends(get_db)
):
    """Refund a completed payment."""
    try:
        service = PaymentService(db)
        payment = service.refund_payment(payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return payment
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{payment_id}", status_code=204)
def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):
    """Delete a payment."""
    service = PaymentService(db)
    success = service.delete_payment(payment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Payment not found")


@router.get("/statistics/overview", response_model=dict)
def get_payment_statistics(
    db: Session = Depends(get_db)
):
    """Get payment statistics."""
    service = PaymentService(db)
    return service.get_payment_statistics()
