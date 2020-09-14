import json
import boto3
from urllib.parse import unquote_plus
from datetime import datetime

def lambda_handler(event, context):
    # TODO implement
    start_step_job(event)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
def start_step_job(event):
    list=[]
    for record in event['Records']:
       key=unquote_plus(record['s3']['object']['key'])
       bucket=record['s3']['bucket']['name']
       print(f'event input s3 Path is :  s3://{bucket}/{key}')
       list.append(f's3://{bucket}/{key}')
    STATE_MACHINE_ARN = 'arn:aws:states:eu-west-1:711533795309:stateMachine:MyStateMachine'

    #The name of the execution
    EXECUTION_NAME = 'MyStateMachine-Exec-'+datetime.now().strftime("%d-%b-%Y-%H-%M-%S")

    #The string that contains the JSON input data for the execution
    INPUT = {"ArgsGeneratedByPreProcessingState":["spark-submit","--deploy-mode","cluster","--class","com.company.project.parquettoCsv","s3://deliverylogs54544322/jars/EMRtest-0.0.1-SNAPSHOT.jar",', '.join(list)]}

    sfn = boto3.client('stepfunctions')

    response = sfn.start_execution(
        stateMachineArn=STATE_MACHINE_ARN,
        name=EXECUTION_NAME,
        input=json.dumps(INPUT))

    #display the arn that identifies the execution
    print(response.get('executionArn'))