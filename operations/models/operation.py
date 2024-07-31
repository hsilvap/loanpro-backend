from sqlmodel import Field,  SQLModel
from typing import  Optional

class Operation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    cost: int
    is_deleted: bool = Field(default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'cost': self.cost
        }
