import os
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import List, Optional

DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)  # email
    active: bool = Field(default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'active': self.active
        }

engine = create_engine(DATABASE_URL)

def get_all_users() -> List[User]:
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users

def get_user(user_id: int) -> Optional[User]:
    with Session(engine) as session:
        user = session.get(User, user_id)
        return user

def create_user(user_data: dict) -> User:
    with Session(engine) as session:
        new_user = User(**user_data)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user

def update_user(user_id: int, user_data: dict) -> Optional[User]:
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            session.commit()
            session.refresh(user)
            return user
    return None
        
    

def delete_user(user_id: int) -> bool:
    with Session(engine) as session:
        user = session.get(User, user_id)
        if user:
            session.delete(user)
            session.commit()
            return True
    return False
