import boto3
from boto3.dynamodb.conditions import Key, Attr
import json

dynamodb = boto3.resource('dynamodb')
client = boto3.client('comprehend')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    ids = event['ID'].split(',')
    id = ids[0]
    
    try:
        table = dynamodb.Table('UnicornFeedback')
        
        for id in ids:
            response_d = table.scan(FilterExpression=Attr('ID').eq(id))
            items = response_d['Items']
            feedback = items[0]['Feedback']
            name = items[0]['Name']
        
            response_c = client.detect_sentiment(Text=feedback, LanguageCode='en')
            sentiment = response_c['Sentiment']
        
            #update the row with sentiment prediction
            table.update_item(
                Key={'Name': name},
                UpdateExpression='SET Sentiment = :val1',
                ExpressionAttributeValues={':val1' : sentiment})
            
        response = table.scan() #get_item(Key={'Name': name})
            
        return response['Items']
    except Exception as e: 
            print("Actual error is: {0}".format(e))