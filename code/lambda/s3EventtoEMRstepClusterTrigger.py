import json
from urllib.parse import unquote_plus
import boto3

def lambda_handler(event, context):
    # TODO implement
     list=[]
     for record in event['Records']:
       key=unquote_plus(record['s3']['object']['key'])
       bucket=record['s3']['bucket']['name']
       print(f'event input s3 Path is :  s3://{bucket}/{key}')
       list.append(f's3://{bucket}/{key}')
     # Send message to SNS
     MY_SNS_TOPIC_ARN = 'arn:aws:sns:eu-west-1:711533795309:EmailSend'
     sns_client = boto3.client('sns')
     sns_client.publish(
        TopicArn = MY_SNS_TOPIC_ARN,
        Subject = 'Recieved files in S3',
        Message = 'list of s3 files  '+ ', '.join(list) + 'and started a emr cluster '+create_emr_step(list) )
        
def create_emr_step(list):
 emrclient = boto3.client('emr')
 cluster_id = emrclient.run_job_flow(
    Name='test_emr_job_boto3',
    LogUri='s3://aws-logs-711533795309-eu-west-1/elasticmapreduce/',
    ReleaseLabel='emr-5.18.0',
    Applications=[
        {
            'Name': 'Spark'
        },
    ],
    Instances={
        'InstanceGroups': [
            {
                'Name': "Master nodes",
                'Market': 'ON_DEMAND',
                'InstanceRole': 'MASTER',
                'InstanceType': 'm4.large',
                'InstanceCount': 1,
            },
            {
                'Name': "Slave nodes",
                'Market': 'SPOT',
                'InstanceRole': 'CORE',
                'InstanceType': 'm4.large',
                'InstanceCount': 1,
            },
            {
                'Name': "Task nodes",
                'Market': 'SPOT',
                'InstanceRole': 'TASK',
                'InstanceType': 'm4.large',
                'InstanceCount': 1,
            }
        ],
        'Ec2KeyName': 'MyEMRKey',
        'KeepJobFlowAliveWhenNoSteps': False,
        'TerminationProtected': False
    },
    Steps=[
        {
            'Name': 'Spark_job',   
                    'ActionOnFailure': 'CONTINUE',
                    'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': ["spark-submit","--deploy-mode","cluster","--class","com.company.project.parquettoCsv","s3://deliverylogs54544322/jars/EMRtest-0.0.1-SNAPSHOT.jar",', '.join(list)]
                    }
        }
    ],
    VisibleToAllUsers=True,
    JobFlowRole='EMR_EC2_DefaultRole',
    ServiceRole='EMR_DefaultRole',
    Tags=[
        {
            'Key': 'project_name',
            'Value': 'tab_value_1',
        },
        {
            'Key': 'tag_name_2',
            'Value': 'tag_value_2',
        },
    ],
 )

 print ('cluster created with the step...', cluster_id['JobFlowId'])
 return cluster_id['JobFlowId']
