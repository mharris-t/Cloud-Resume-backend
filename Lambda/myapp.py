import json
import boto3
import os
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
# Set dynamodb table name variable from OS environment
ddbTableName = os.environ['databaseName']
table = dynamodb.Table(ddbTableName)

def decimal_default_proc(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def myLambdaCounter(event, context):

    ddbResponse = table.update_item(
        Key={
            "id": "WebsiteCounter"
        },
        UpdateExpression='ADD visits :inc',
        ExpressionAttributeValues={
            ':inc': 1
        },
        ReturnValues="UPDATED_NEW"
    )

    # DynamoDB response is converted to JSON
    responseBody = json.dumps({"WebsiteCounter": ddbResponse["Attributes"]["visits"]},default=decimal_default_proc)

    #Interfacing API gateway
    API_GatewayResponse = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": responseBody,
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS" 
        },        
    }

    return API_GatewayResponse