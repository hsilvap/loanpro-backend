import os
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import List, Optional

DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

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

engine = create_engine(DATABASE_URL)


def get_all_operations() -> List[Operation]:
    with Session(engine) as session:
        statement = select(Operation).where(Operation.is_deleted == False)
        results = session.exec(statement)
        return results.all()

def get_operation(operation_id: int) -> Optional[Operation]:
    with Session(engine) as session:
        statement = select(Operation).where(Operation.id == operation_id, Operation.is_deleted == False)
        return session.exec(statement).first()

def create_operation(operation_data: dict) -> Operation:
    with Session(engine) as session:
        new_operation = Operation(**operation_data)
        session.add(new_operation)
        session.commit()
        session.refresh(new_operation)
        return new_operation

def update_operation(operation_id: int, operation_data: dict) -> Optional[Operation]:
    with Session(engine) as session:
        operation = session.get(Operation, operation_id)
        if operation and not operation.is_deleted:
            for key, value in operation_data.items():
                setattr(operation, key, value)
            session.commit()
            session.refresh(operation)
            return operation
    return None

def delete_operation(operation_id: int) -> bool:
    with Session(engine) as session:
        operation = session.get(Operation, operation_id)
        if operation and not operation.is_deleted:
            operation.is_deleted = True
            session.commit()
            return True
    return False