from sqlmodel import Field, SQLModel, Relationship
from typing import  Optional, List

class Operation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    cost: int
    is_deleted: bool = Field(default=False)
    
