import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
import uuid

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    firstname = event['FirstName']
    lastname = event['LastName']
    feedback = event['Feedback']
    
    #print('Test UUID: ' + str(uuid.uuid4()))
    
    try:
        table = dynamodb.Table('UnicornFeedback')
        table.put_item(
            Item ={'FirstName': firstname,
                   'LastName': lastname,
                   'Name': firstname + ' ' + lastname,
                   'Feedback': feedback,
                   'ID': str(uuid.uuid4())
            })
        
        return 'Hello from Lambda'
    except Exception as e: 
            print("Actual error is: {0}".format(e))