from sqlmodel import Field,  SQLModel
from typing import   Optional

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
