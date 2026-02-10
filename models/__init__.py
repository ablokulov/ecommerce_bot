from .base import Base
from .user import User
from .product import Product
from .category import Category
from .cart import Cart,CartItem
from .order import Order,OrderItem

from database.connection import engine
from models.base import Base


Base.metadata.create_all(bind=engine)     # Bu Hmma yozgan classlarimni databasega migration qiladi 