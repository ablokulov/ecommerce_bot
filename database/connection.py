from sqlalchemy import URL,create_engine
from config import (
    DB_NAME,
    DB_USER,
    DB_PASS,
    DB_PORT,
    DB_HOST,
)


DATABASE_URL = URL.create(
    "postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASS,
    database=DB_NAME,
    port=DB_PORT,
    host=DB_HOST
)

engine = create_engine(DATABASE_URL)
