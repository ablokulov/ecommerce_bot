from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    BigInteger,
    DateTime  
)

from models.base import Base


class User(Base):
    __tablename__ = "users"
    
    user_id = Column("id", BigInteger, index=True, primary_key=True)
    telegram_id = Column("telegram_id", BigInteger, unique=True)
    full_name = Column("full_name",String(150),nullable=False)
    phone_number = Column("phone_number",String(20))
    created_at = Column("created_at",DateTime,default=datetime.utcnow)

