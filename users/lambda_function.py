import os
import logging
import json
from services.service import get_all_users, get_user,create_user,update_user,delete_user

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

def lambda_handler(event, context):
    logger.debug(event)
    
    try:
        
        if event['httpMethod'] == 'GET':
            user_id = event['pathParameters'].get('id') if event.get('pathParameters') else None
            if user_id:
                user = get_user(int(user_id))
                if user:
                    return {
                        'statusCode': 200,
                        'body': json.dumps(user.to_dict()),
                        'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                        },
                    }
                else:
                    return {
                        'statusCode': 404,
                        'body': json.dumps({'error': 'User not found'}),
                        'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                        },
                    }
            else:
                users = get_all_users()
                return {
                    'statusCode': 200,
                    'body': json.dumps([user.to_dict() for user in users]),
                    'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                    },
                }
        
        elif event['httpMethod']  == 'POST':
            user_data = json.loads(event['body'])
            new_user = create_user(user_data)
            return {
                'statusCode': 201,
                'body': json.dumps(new_user.to_dict()),
                'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                },
            }
        
        elif event['httpMethod']  == 'PUT':
            user_id = event['pathParameters']['id']
            user_data = json.loads(event['body'])
            updated_user = update_user(int(user_id), user_data)
            if updated_user:
                return {
                    'statusCode': 200,
                    'body': json.dumps(updated_user.to_dict()),
                    'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                    },
                }
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'User not found'}),
                    'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                    },
                }
        
        elif event['httpMethod']  == 'DELETE':
            user_id = event['pathParameters']['id']
            if delete_user(int(user_id)):
                return {
                    'statusCode': 204,
                    'body': '',
                    'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                    },
                }
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'User not found'}),
                    'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                    },
                }
        
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid request'}),
                'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                },
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
            },
        }