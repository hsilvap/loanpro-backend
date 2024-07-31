from sqlmodel import Field, SQLModel, Relationship
from typing import  Optional
from datetime import datetime
from models.operation import Operation
class Record(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    operation_id: int = Field(foreign_key="operation.id")

    user_id: int
    amount: int
    user_balance: int
    operation_response: str
    date: datetime = Field(default_factory=datetime.now)
    is_deleted: bool = Field(default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'operation_id': self.operation_id,
            'user_id': self.user_id,
            'amount': self.amount,
            'user_balance': self.user_balance,
            'operation_response': self.operation_response,
            'date': self.date.isoformat(),
        }
