from sqlalchemy.orm import Session
from models import Product


class ProductRepository:
    
    def __init__(self,session:Session):
        self.session = session
        
        
    def create_product(self,name:str,description:str,price,stock:int,image_url:str,category_id:int):
        
        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            image_url=image_url,
            category_id=category_id
        )
        
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)

        return product