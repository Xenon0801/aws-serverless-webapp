import json
import boto3
import uuid
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

def lambda_handler(event, context):
    http_method = event.get('httpMethod', '')
    path_params = event.get('pathParameters') or {}
    body = json.loads(event.get('body') or '{}')

    if http_method == 'POST':
        # CREATE user
        user_id = str(uuid.uuid4())
        item = {'id': user_id, **body}
        table.put_item(Item=item)
        return response(201, {'message': 'User created', 'id': user_id})

    elif http_method == 'GET' and path_params.get('id'):
        # GET single user
        result = table.get_item(Key={'id': path_params['id']})
        item = result.get('Item')
        if not item:
            return response(404, {'message': 'User not found'})
        return response(200, item)

    elif http_method == 'GET':
        # LIST all users
        result = table.scan()
        return response(200, result.get('Items', []))

    elif http_method == 'PUT' and path_params.get('id'):
        # UPDATE user
        table.put_item(Item={'id': path_params['id'], **body})
        return response(200, {'message': 'User updated'})

    elif http_method == 'DELETE' and path_params.get('id'):
        # DELETE user
        table.delete_item(Key={'id': path_params['id']})
        return response(200, {'message': 'User deleted'})

    return response(400, {'message': 'Unsupported method'})

def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(body, default=str)
    }
