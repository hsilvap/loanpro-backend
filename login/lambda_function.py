import os
import logging
from sqlmodel import  Field, Session, SQLModel, create_engine, select
from typing import  Optional

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

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
        
def lambda_handler(event, context):
    logger.debug(event)
    
    try:
        email = event['request']['userAttributes']['email']
    except KeyError as e:
        logger.error(f"Failed to extract email from event: {e}")
        return event
    
    try:
         with Session(engine) as session:
            statement = select(User).where(User.username == email, User.active == True)
            user = session.exec(statement).first()
            
            if user:
                logger.info(f"User {email} found and active")
                event['response'] = event.get('response', {})
                event['response']['claimsOverrideDetails'] = {
                    'claimsToAddOrOverride': {
                        'custom:user_id': str(user.id)
                    }
                }
            else:
                logger.warning(f"User {email} not found or not active")
                
               
    except Exception as e:
          print(f"ERROR: Unexpected error: {str(e)}")
    return event