import os
import logging
import json
from services.service import get_all_operations, get_operation,create_operation,update_operation,delete_operation

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


def lambda_handler(event, context):

    logger.debug(event)
    try:
        
        if event['httpMethod'] == 'GET':
            operation_id = event['pathParameters'].get('id') if event.get('pathParameters') else None
            if operation_id:
                operation = get_operation(int(operation_id))
                if operation:
                    return {
                        'statusCode': 200,
                        'body': json.dumps(operation.to_dict()),
                        'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                        },
                    }
                else:
                    return {
                        'statusCode': 404,
                        'body': json.dumps({'error': 'Operation not found'}),
                        'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                        },
                    }
            else:
                operations = get_all_operations()
                return {
                    'statusCode': 200,
                    'body': json.dumps([op.to_dict() for op in operations]),
                    'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                        },
                }
        
        elif event['httpMethod']  == 'POST':
            operation_data = json.loads(event['body'])
            new_operation = create_operation(operation_data)
            return {
                'statusCode': 201,
                'body': json.dumps(new_operation.to_dict()),
                'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                        },
            }
        
        elif event['httpMethod']  == 'PUT':
            operation_id = event['pathParameters']['id']
            operation_data = json.loads(event['body'])
            updated_operation = update_operation(int(operation_id), operation_data)
            if updated_operation:
                return {
                    'statusCode': 200,
                    'body': json.dumps(updated_operation.to_dict()),
                    'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                        },
                }
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'Operation not found'}),
                    'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                        },
                }
        
        elif event['httpMethod']  == 'DELETE':
            operation_id = event['pathParameters']['id']
            if delete_operation(int(operation_id)):
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
                    'body': json.dumps({'error': 'Operation not found'}),
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