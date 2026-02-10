from fastapi import APIRouter
from .food import router as food_router
from .order import router as order_router
from .payment import router as payment_router
from .promotion import router as promotion_router
from .qr_code import router as qr_code_router

api_router = APIRouter()

api_router.include_router(food_router, prefix="/foods", tags=["foods"])
api_router.include_router(order_router, prefix="/orders", tags=["orders"])
api_router.include_router(payment_router, prefix="/payments", tags=["payments"])
api_router.include_router(promotion_router, prefix="/promotions", tags=["promotions"])
api_router.include_router(qr_code_router, prefix="/qr", tags=["qr-codes"])

__all__ = ["api_router"]
