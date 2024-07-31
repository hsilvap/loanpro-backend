import json
import boto3
import os
from typing import  Optional
from sqlmodel import  Session,  create_engine, select, func
from sqlalchemy import Integer, Numeric, DateTime, Date, Boolean
from services.operations import calculate
from models.record import Record

DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
# can be saved as a env var.
INITIAL_CREDITS = 100


engine = create_engine(DATABASE_URL)

def get_records(page: int = 1, per_page: int = 10, sort_by: str = 'id', sort_order: str = 'asc') -> dict:
    with Session(engine) as session:
        query = select(Record).where(Record.is_deleted == False)
        
        if hasattr(Record, sort_by):
            order_column = getattr(Record, sort_by)
            
            if isinstance(order_column.type, (Integer, Numeric)):
                order_column = func.cast(order_column, Numeric)
            elif isinstance(order_column.type, (DateTime, Date)):
                order_column = func.cast(order_column, DateTime)
            elif isinstance(order_column.type, Boolean):
                order_column = func.cast(order_column, Boolean)

            if sort_order.lower() == 'desc':
                query = query.order_by(order_column.desc())
            else:
                query = query.order_by(order_column.asc())
       
        total = session.exec(select(func.count()).select_from(query.subquery())).one()
        query = query.offset((page - 1) * per_page).limit(per_page)
        
        records = session.exec(query).all()
        
        return {
            'records': [record.to_dict() for record in records],
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page
        }

def get_record(record_id: int) -> Optional[Record]:
    with Session(engine) as session:
        record = session.exec(select(Record).where(Record.id == record_id, Record.is_deleted == False)).first()
        return record

def get_user_last_record(user_id: int) -> Optional[Record]:
    with Session(engine) as session:
        last_record = session.exec(
            select(Record)
            .where(Record.user_id == user_id, Record.is_deleted == False)
            .order_by(Record.date.desc())
        ).first()
        return last_record

def create_record(record_data: dict) -> Record:
    with Session(engine) as session:
        new_record = Record(**record_data)
        session.add(new_record)
        session.commit()
        session.refresh(new_record)
        return new_record

def update_record(record_id: int, record_data: dict) -> Optional[Record]:
    with Session(engine) as session:
        record = session.exec(select(Record).where(Record.id == record_id, Record.is_deleted == False)).first()
        if record:
            for key, value in record_data.items():
                setattr(record, key, value)
            session.commit()
            session.refresh(record)
        return record

def delete_record(record_id: int) -> bool:
    with Session(engine) as session:
        record = session.exec(select(Record).where(Record.id == record_id, Record.is_deleted == False)).first()
        if record:
            record.is_deleted = True
            session.commit()
            return True
    return False



class MissingFieldError(Exception):
    pass

class InsufficientCreditsError(Exception):
    pass

def perform_calculation(data):
    required_fields = ['user_id', 'operation_id']
    for field in required_fields:
        if field not in data:
            raise MissingFieldError(f'Missing required field: {field}')
    
    user_id = data['user_id']
    operation_id = data['operation_id']
    first_input = data['first_input']
    second_input = data['second_input']
    
    lambda_client = boto3.client('lambda')
    
    payload = {
        "httpMethod":"GET",
        "pathParameters": { "id":operation_id} 
    }
    
    try:
        response = lambda_client.invoke(
            FunctionName='arn:aws:lambda:us-east-2:010438465735:function:operations',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        payload = json.loads(response['Payload'].read())
        operation =  json.loads(payload.get('body'))
    except Exception as e:
        raise RuntimeError('Failed to invoke operations Lambda',str(e))
    
    last_record = get_user_last_record(user_id)
    if last_record:
        new_balance = last_record.user_balance - operation['cost']
    else:
        new_balance = INITIAL_CREDITS - operation['cost']
        
    if new_balance < 0:
        raise InsufficientCreditsError('Insufficient credits')
    
    result = calculate(operation['type'],first_input,second_input)
    try:
        create_record({"user_id":user_id, "operation_id":operation_id, "amount":operation['cost'], "user_balance":new_balance,"operation_response": result})
    except Exception as e:
        raise RuntimeError('Failed to persist record',str(e))
    return  result
    