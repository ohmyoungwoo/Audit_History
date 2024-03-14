from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from model.models import User

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def create_user(db: Session, user_create: UserCreate):
    db_user = User(username = user_create.username,
                   password = pwd_context.hash(user_create.password1),
                   email=user_create.email,
                   no_company = user_create.no_company)
    
    db.add(db_user)
    db.commit()
    
def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.username == user_create.username) |
        (User.email == user_create.email) |
        (User.no_company == user_create.no_company)
    ).first()