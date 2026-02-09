from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Food(Base):
    """Food model representing a food item in the shop."""
    
    __tablename__ = "foods"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    category = Column(String(100), index=True, nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Food(id={self.id}, name={self.name}, price={self.price})>"
