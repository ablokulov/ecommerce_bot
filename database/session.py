from sqlalchemy.orm import sessionmaker
from database.connection import engine

SessionLocal = sessionmaker(bind=engine)


print(SessionLocal)