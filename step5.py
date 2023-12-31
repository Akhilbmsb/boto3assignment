
import boto3
import os

# Schedule the Lambda function to run every 5 minutes
cloudwatch = boto3.client('cloudwatch')

cloudwatch.put_rule(
    Name='health-check-schedule',
    ScheduleExpression='rate(5 minutes)',
    State='ENABLED',
    Targets=[{
        'Id': 'web-app-health-check',
        'Arn': 'arn:aws:lambda:ap-south-1:295397358094:function:webapphealth'  # Replace with your Lambda function ARN
    }]
)
