import boto3
from boto3.dynamodb.conditions import Key, Attr
import json

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
     
    try:
        table = dynamodb.Table('UnicornFeedback')
        
        response = table.scan()
        items = response['Items']
        return items
    except Exception as e: 
            print("Actual error is: {0}".format(e))