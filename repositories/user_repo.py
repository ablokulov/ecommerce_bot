from sqlalchemy.orm import Session
from models import User


class  UserRepository:
    
    def __init__(self,session:Session):
        self.session = session
        
    def get_by_telegram_id(self,telegram_id:int):
        return (self.session.query(User).filter(User.telegram_id == telegram_id).first())
    
    
    def create_user(self, telegram_id :int, full_name :str):
        
        user = User(telegram_id=telegram_id,full_name=full_name)
        
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        
        return user
    
    def get_or_create_user(self,telegram_id: int, full_name: str):
        
        user = self.get_by_telegram_id(telegram_id)
        
        if user:
            return user
        
        return self.create_user(telegram_id,full_name)