import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
import re

dynamodb = boto3.resource('dynamodb')
client = boto3.client('comprehend')
sagemaker = boto3.client('sagemaker-runtime')

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
            first_name = items[0]['FirstName']

            response = sagemaker.invoke_endpoint(
                EndpointName='tf-names-2018-03-21-16-48-01-322',
                Body='{"name":"' + first_name + '"}',
                ContentType='application/json',
                Accept='*/*')
            
            body = response['Body']
            json_str = body.read()
            json_data = json.loads(json_str)
            outputs = json_data['outputs']
            gender = outputs['Gender']
            
            prediction = str(gender['floatVal']).strip('[]')
            gender = "Male" if float(prediction) < 0.5 else "Female"
        
            #update the row with sentiment prediction
            table.update_item(
                Key={'Name': name},
                UpdateExpression='SET Gender = :val1',
                ExpressionAttributeValues={':val1' : gender})
            
        response = table.scan() 
            
        return response['Items']
    except Exception as e: 
        print("Actual error is: {0}".format(e))
