from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class PaymentMethodEnum(str, enum.Enum):
    """Available payment methods."""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    APPLE_PAY = "apple_pay"
    GOOGLE_PAY = "google_pay"
    BANK_TRANSFER = "bank_transfer"
    CASH = "cash"


class PaymentStatusEnum(str, enum.Enum):
    """Payment status states."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class Payment(Base):
    """Payment model representing a payment transaction."""
    
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    payment_method = Column(SQLEnum(PaymentMethodEnum), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(SQLEnum(PaymentStatusEnum), default=PaymentStatusEnum.PENDING, nullable=False)
    transaction_id = Column(String(255), unique=True, nullable=True)
    reference_number = Column(String(255), unique=True, nullable=True)
    card_last_four = Column(String(4), nullable=True)  # For card payments
    notes = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Payment(id={self.id}, order_id={self.order_id}, status={self.status})>"
