import json
import boto3
from urllib.parse import unquote_plus
from datetime import datetime

def lambda_handler(event, context):
    # TODO implement
    print(event)
    send_email(event)
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
def send_email(event):
    MY_SNS_TOPIC_ARN = 'arn:aws:sns:eu-west-1:711533795309:EmailSend'
    sns_client = boto3.client('sns')
    sns_client.publish(
        TopicArn = MY_SNS_TOPIC_ARN,
        Subject = 'EMR job Status',
        Message = "EMR job Status json output: \n"+ json.dumps(event) )