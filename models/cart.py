from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    String,
    BigInteger,
    DateTime,
    ForeignKey,
    Integer
)

from models.base import Base

class Cart(Base):
    
    __tablename__ = "carts"
    
    id = Column(BigInteger,primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, unique=True)
    
    user = relationship("User",back_populates="cart")
    
    items = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan"
    )
    
    created_at = Column(DateTime(timezone=True),default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True),default=datetime.utcnow,onupdate=datetime.utcnow)
    


class CartItem(Base):
    
    __tablename__ = "cartitems"
    
    id = Column(BigInteger,primary_key=True)
    cart_id = Column(BigInteger,ForeignKey("carts.id"),nullable=False,unique=True)
    product_id = Column(BigInteger,ForeignKey("products.id"),nullable=False)
    quantity = Column(Integer,nullable=False,default=1)
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")
    
    created_at = Column(DateTime(timezone=True),default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True),default=datetime.utcnow,onupdate=datetime.utcnow)
    