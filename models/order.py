import enum 
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    String,
    BigInteger,
    DateTime,
    ForeignKey,
    Numeric,
    Enum,
    Integer
)

from models import Base


class Status(enum.Enum):
    PENDING = "pending"
    RECEIVED = "received"
    COMPLETED = "completed"
    

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(BigInteger,primary_key=True)
    user_id = Column(BigInteger,ForeignKey('users.id'),index=True,nullable=False)
    total_price = Column(Numeric(10,2), nullable=False)
    status = Column(Enum(Status),default=Status.PENDING,nullable=False)
    phone_number = Column(String(20), nullable=False)
    delivery_address = Column(String,nullable=False)
    
    user = relationship("User",backref="orders")
    
    
    items = relationship("OrderItem",back_populates="order",cascade="all, delete-orphan"
    )
    
    
    created_at = Column(DateTime(timezone=True),default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True),default=datetime.utcnow,onupdate=datetime.utcnow)
    
    
class OrderItem(Base):
    __tablename__ = "orderitems"  
    
    id = Column(BigInteger,primary_key=True)
    order_id = Column(BigInteger,ForeignKey("orders.id"),index=True,nullable=False)
    product_id = Column(BigInteger,ForeignKey("products.id"),index=True,nullable=False)
    quantity  = Column(Integer,nullable=False)
    price_snapshot = Column(Numeric(10,2),nullable=False)
    
    order = relationship("Order", back_populates="items"
    )
    
    created_at = Column(DateTime(timezone=True),default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True),default=datetime.utcnow,onupdate=datetime.utcnow)
    
    
    
    
    
