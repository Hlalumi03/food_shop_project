from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import OrderService
from app.schemas import OrderCreate, OrderUpdate, OrderResponse
from typing import List

router = APIRouter()


@router.post("", response_model=OrderResponse, status_code=201)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):
    """Create a new order."""
    try:
        service = OrderService(db)
        order = service.create_order(order_data)
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    """Get an order by ID."""
    service = OrderService(db)
    order = service.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.get("", response_model=List[OrderResponse])
def get_all_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    email: str = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    """Get all orders or filter by email/status."""
    service = OrderService(db)
    
    if email:
        orders = service.get_orders_by_customer(email, skip, limit)
    elif status:
        if status not in ["pending", "confirmed", "delivered"]:
            raise HTTPException(status_code=400, detail="Invalid status")
        orders = service.get_orders_by_status(status, skip, limit)
    else:
        orders = service.get_all_orders(skip, limit)
    
    return orders


@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_data: OrderUpdate,
    db: Session = Depends(get_db)
):
    """Update an order."""
    service = OrderService(db)
    order = service.update_order(order_id, order_data)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch("/{order_id}/confirm", response_model=OrderResponse)
def confirm_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    """Confirm an order."""
    service = OrderService(db)
    order = service.confirm_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch("/{order_id}/deliver", response_model=OrderResponse)
def mark_as_delivered(
    order_id: int,
    db: Session = Depends(get_db)
):
    """Mark an order as delivered."""
    service = OrderService(db)
    order = service.mark_as_delivered(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch("/{order_id}/pay", response_model=OrderResponse)
def mark_as_paid(
    order_id: int,
    db: Session = Depends(get_db)
):
    """Mark an order as paid."""
    service = OrderService(db)
    order = service.mark_as_paid(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete("/{order_id}", status_code=204)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    """Delete an order."""
    service = OrderService(db)
    success = service.delete_order(order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
