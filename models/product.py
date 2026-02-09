from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    String,
    BigInteger,
    DateTime,
    ForeignKey,
    Text,
    Numeric,
    Integer,
    Boolean
)

from models.base import Base


class Product(Base):
    __tablename__ = "products"
    
    id = Column(BigInteger, primary_key=True)
    name = Column(String(150),nullable=False)
    description = Column(Text)
    price = Column(Numeric(10,2),nullable=False)
    stock = Column(Integer,nullable=False,default=0)
    image_url = Column(String,nullable=False,default="https://www.tiffincurry.ca/wp-content/uploads/2021/02/default-product.png")
    category_id = Column(BigInteger,ForeignKey("categories.id"),nullable=False,index=True)
    is_activ = Column(Boolean,default=True)
    
    category = Column(relationship("Category",backref="products"))
    
    created_at = Column(DateTime(timezone=True),default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True),default=datetime.utcnow,onupdate=datetime.utcnow)
    
    