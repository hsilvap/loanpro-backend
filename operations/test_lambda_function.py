import unittest
import json
import os
from unittest.mock import patch

# Set environment variables before importing the module
os.environ['DB_USER'] = 'test_user'
os.environ['DB_PASSWORD'] = 'test_password'
os.environ['DB_HOST'] = 'test_host'
os.environ['DB_NAME'] = 'test_db'


from lambda_function import lambda_handler
from services.service import Operation

class TestLambdaHandler(unittest.TestCase):

  
    @patch('lambda_function.get_all_operations')
    def test_get_all_operations(self, mock_get_all):
        mock_operations = [
            Operation(id=1, type='Type1', cost=100),
            Operation(id=2, type='Type2', cost=200)
        ]
        mock_get_all.return_value = mock_operations

        event = {'httpMethod': 'GET'}
        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertEqual(len(body), 2)
        self.assertEqual(body[0]['id'], 1)
        self.assertEqual(body[1]['id'], 2)

    @patch('lambda_function.get_operation')
    def test_get_specific_operation(self, mock_get):
        mock_operation = Operation(id=1, type='Type1', cost=100)
        mock_get.return_value = mock_operation

        event = {
            'httpMethod': 'GET',
            'pathParameters': {'id': '1'}
        }
        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertEqual(body['id'], 1)
        self.assertEqual(body['type'], 'Type1')

    @patch('lambda_function.get_operation')
    def test_get_nonexistent_operation(self, mock_get):
        mock_get.return_value = None

        event = {
            'httpMethod': 'GET',
            'pathParameters': {'id': '999'}
        }
        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 404)
        body = json.loads(response['body'])
        self.assertEqual(body['error'], 'Operation not found')

    @patch('lambda_function.create_operation')
    def test_create_operation(self, mock_create):
        mock_operation = Operation(id=1, type='NewType', cost=300)
        mock_create.return_value = mock_operation

        event = {
            'httpMethod': 'POST',
            'body': json.dumps({'type': 'NewType', 'cost': 300})
        }
        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 201)
        body = json.loads(response['body'])
        self.assertEqual(body['id'], 1)
        self.assertEqual(body['type'], 'NewType')
        self.assertEqual(body['cost'], 300)

    @patch('lambda_function.update_operation')
    def test_update_operation(self, mock_update):
        mock_operation = Operation(id=1, type='UpdatedType', cost=400)
        mock_update.return_value = mock_operation

        event = {
            'httpMethod': 'PUT',
            'pathParameters': {'id': '1'},
            'body': json.dumps({'type': 'UpdatedType', 'cost': 400})
        }
        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertEqual(body['id'], 1)
        self.assertEqual(body['type'], 'UpdatedType')
        self.assertEqual(body['cost'], 400)

    @patch('lambda_function.update_operation')
    def test_update_nonexistent_operation(self, mock_update):
        mock_update.return_value = None

        event = {
            'httpMethod': 'PUT',
            'pathParameters': {'id': '999'},
            'body': json.dumps({'type': 'UpdatedType', 'cost': 400})
        }
        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 404)
        body = json.loads(response['body'])
        self.assertEqual(body['error'], 'Operation not found')

    @patch('lambda_function.delete_operation')
    def test_delete_operation(self, mock_delete):
        mock_delete.return_value = True

        event = {
            'httpMethod': 'DELETE',
            'pathParameters': {'id': '1'}
        }
        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 204)
        self.assertEqual(response['body'], '')

    @patch('lambda_function.delete_operation')
    def test_delete_nonexistent_operation(self, mock_delete):
        mock_delete.return_value = False

        event = {
            'httpMethod': 'DELETE',
            'pathParameters': {'id': '999'}
        }
        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 404)
        body = json.loads(response['body'])
        self.assertEqual(body['error'], 'Operation not found')

    def test_invalid_http_method(self):
        event = {'httpMethod': 'PATCH'}
        response = lambda_handler(event, None)

        self.assertEqual(response['statusCode'], 400)
        body = json.loads(response['body'])
        self.assertEqual(body['error'], 'Invalid request')


if __name__ == '__main__':
    unittest.main()