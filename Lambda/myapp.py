import json
import boto3
import os
from decimal import Decimal


# circumventing decimal error. Could use int/float as well.
def decimal_default_proc(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

#defining interaction event with dynamodb
def mydynamofunc():
    dynamodb = boto3.resource('dynamodb')
    ddbTableName = os.environ['databaseName']
    table = dynamodb.Table(ddbTableName)

    dynamoevent = table.update_item(
        Key={
            "id": "WebsiteCounter"
        },
        UpdateExpression='ADD visits :inc',
        ExpressionAttributeValues={
            ':inc': 1
        },
        ReturnValues="UPDATED_NEW"
    )
    return dynamoevent
    
#lambda function is defined here
def myLambdaCounter(event, context):
#engage event here from mydynamo function
    dbEvent = mydynamofunc()
    # DynamoDB response is converted to JSON
    responseBody = json.dumps({"WebsiteCounter": dbEvent["Attributes"]["visits"]},default=decimal_default_proc)
    #Interfacing API gateway by sending the necessary headers and payload
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