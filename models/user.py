from datetime import datetime
from sqlalchemy.orm  import relationship
from sqlalchemy import (
    Column,
    String,
    BigInteger,
    DateTime  
)

from models import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(BigInteger, index=True, primary_key=True)
    telegram_id = Column(BigInteger, index=True, unique=True)
    full_name = Column(String(150),nullable=False)
    phone_number = Column(String(20))
    
    cart = relationship(
        "Cart",
        back_populates="user"
    )
    created_at = Column(DateTime(timezone=True),default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True),default=datetime.utcnow,onupdate=datetime.utcnow)
    

