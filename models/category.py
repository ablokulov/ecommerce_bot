from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    String,
    BigInteger,
    DateTime,
    ForeignKey
)

from models import Base


class Category(Base):
    __tablename__ = "categories"
    
    id = Column(BigInteger,primary_key=True)
    name = Column(String(150),nullable=False)
    parent_id = Column(BigInteger,ForeignKey("categories.id"))
    parent = relationship("Category",remote_side=[id],backref="children")
    
    created_at = Column(DateTime(timezone=True),default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True),default=datetime.utcnow,onupdate=datetime.utcnow)
    

    