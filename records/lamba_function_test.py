import unittest
import json
import os
import sys
from unittest.mock import patch, MagicMock

sys.modules['boto3'] = MagicMock()
os.environ['DB_USER'] = 'test_user'
os.environ['DB_PASSWORD'] = 'test_password'
os.environ['DB_HOST'] = 'test_host'
os.environ['DB_NAME'] = 'test_db'

from lambda_function import lambda_handler,MissingFieldError, InsufficientCreditsError

class TestLambdaHandler(unittest.TestCase):
    @patch('lambda_function.get_record')
    def test_get_single_record(self, mock_get_record):
        mock_record = MagicMock()
        mock_record.to_dict.return_value = {'id': 1, 'name': 'Test Record'}
        mock_get_record.return_value = mock_record

        event = {
            'httpMethod': 'GET',
            'pathParameters': {'id': '1'},
        }

        response = lambda_handler(event, {})

        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(json.loads(response['body']), {'id': 1, 'name': 'Test Record'})

    @patch('lambda_function.get_records')
    def test_get_all_records(self, mock_get_records):
        mock_records = [MagicMock(), MagicMock()]
        mock_records[0].to_dict.return_value = {'id': 1, 'name': 'Record 1'}
        mock_records[1].to_dict.return_value = {'id': 2, 'name': 'Record 2'}
        mock_get_records.return_value = mock_records

        event = {
            'httpMethod': 'GET',
            'queryStringParameters': None,
        }

        response = lambda_handler(event, {})

        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(json.loads(response['body']), [{'id': 1, 'name': 'Record 1'}, {'id': 2, 'name': 'Record 2'}])
        
    @patch('lambda_function.get_records')
    def test_get_records_with_params(self,mock_get_records):
        mock_get_records.return_value = {'data': [{'id': 1, 'name': 'Record 1'}], 'total': 1, 'page': 1, 'total':1}

        event = {
                'httpMethod': 'GET',
                'queryStringParameters': {
                    'page': '1',
                    'per_page': '10',
                    'sort_by': 'name',
                    'sort_order': 'desc',
                    'user_id': '1',
                    'search': 'test'
                },
            }

        response = lambda_handler(event, {})

        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(json.loads(response['body']), {'data': [{'id': 1, 'name': 'Record 1'}], 'total': 1, 'page': 1, 'total':1})

    @patch('lambda_function.create_record')
    def test_create_record(self, mock_create_record):
        mock_record = MagicMock()
        mock_record.to_dict.return_value = {'id': 1, 'name': 'New Record'}
        mock_create_record.return_value = mock_record

        event = {
            'httpMethod': 'POST',
            'body': json.dumps({'name': 'New Record'}),
        }

        response = lambda_handler(event, {})

        self.assertEqual(response['statusCode'], 201)
        self.assertEqual(json.loads(response['body']), {'id': 1, 'name': 'New Record'})
        
    @patch('lambda_function.perform_calculation')
    def test_insufficient_credits_error(self, mock_perform_calculation):
        mock_perform_calculation.side_effect = InsufficientCreditsError('Not enough credits')

        event = {
            'httpMethod': 'POST',
            'path': '/calculate',
            'body': json.dumps({'operation': 'complex_calc'}),
        }

        response = lambda_handler(event, {})

        self.assertEqual(response['statusCode'], 403)
        self.assertEqual(json.loads(response['body']), {'error': 'Not enough credits'})

    @patch('lambda_function.perform_calculation')
    def test_missing_field_error(self, mock_create_record):
        mock_create_record.side_effect = MissingFieldError('user_id is required')

        event = {
            'httpMethod': 'POST',
            'path': '/calculate',
            'body': json.dumps({}),
        }

        response = lambda_handler(event, {})

        self.assertEqual(response['statusCode'], 400)
        self.assertEqual(json.loads(response['body']), {'error': 'user_id is required'})
        
if __name__ == '__main__':
    unittest.main()