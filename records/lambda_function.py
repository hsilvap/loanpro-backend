import os
import logging
import json
from services.service import get_records,get_record,create_record,update_record,delete_record,perform_calculation,MissingFieldError,InsufficientCreditsError

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

def lambda_handler(event, context):
    logger.debug(event)
    
    try:
        path = event.get('path', '')

        if event['httpMethod'] == 'GET':
            operation_id = event['pathParameters'].get('id') if event.get('pathParameters') else None
            if operation_id:
                record = get_record(int(operation_id))
                if record:
                    return {
                        'statusCode': 200,
                        'body': json.dumps(record.to_dict()),
                        'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                        },
                    }
                else:
                    return {
                        'statusCode': 404,
                        'body': json.dumps({'error': 'Record not found'}),
                        'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                        },
                    }
            else:
                query_params = event.get('queryStringParameters', {}) or {}
                page = int(query_params.get('page', 1))
                per_page = int(query_params.get('per_page', 10))
                sort_by = query_params.get('sort_by', 'id')
                sort_order = query_params.get('sort_order', 'asc')
                
                records = get_records(page, per_page, sort_by, sort_order)
                return {
                    'statusCode': 200,
                    'body': json.dumps(records),
                    'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                        },
                }
        
        elif event['httpMethod']  == 'POST':
            if path.endswith('/calculate'):
                operation_data = json.loads(event['body'])
                result = perform_calculation(operation_data)
                return {
                    'statusCode': 200,
                    'body': json.dumps({'result': result}),
                    'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                    },
                }
            else:
                operation_data = json.loads(event['body'])
                new_operation = create_record(operation_data)
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
            updated_operation = update_record(int(operation_id), operation_data)
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
            if delete_record(int(operation_id)):
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

    
    except MissingFieldError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                        },
        }
    except InsufficientCreditsError as e:
        return {
            'statusCode': 403,
            'body': json.dumps({'error': str(e)}),
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