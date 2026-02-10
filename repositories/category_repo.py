from sqlalchemy.orm import Session
from models import Category


class CategoryRepostoriy:
    
    def __init__(self,session: Session):
        self.session = session
        
        
    def create_category(self,name: str):
        
        category = Category(
            name=name
        )
        
        self.session.add(category)
        self.session.commit()
        self.session.refresh(category)
        
        return category