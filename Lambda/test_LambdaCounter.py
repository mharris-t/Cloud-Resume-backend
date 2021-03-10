import boto3
import os
import pytest
from moto import mock_dynamodb2
myTableName = os.environ['databaseName'] = 'testing'
from myapp import myLambdaCounter

#initialize mockdynamodb table
@pytest.fixture
def moto_init():
    @mock_dynamodb2
    def dynamodb_client():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        dynamodb.create_table(
            TableName = myTableName,
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
            ],
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                },
            ]
        )    
        return dynamodb
    return dynamodb_client

#testing the lambda function
@mock_dynamodb2
def test_handler_ok(moto_init):
    moto_init()
    return_data = myLambdaCounter(0,0)
    print(return_data)    
    assert return_data['statusCode'] == 200




            


