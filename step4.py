import boto3
import os
# Initialize the Lambda client
lambda_client = boto3.client('lambda')

# Create a Lambda function
lambda_client.create_function(
    FunctionName='web-app-health-check',
    Runtime='python3.8',
    Role='arn:aws:iam::295397358094:role/Madan_Lambda_EC2_Role',  # Replace with your Lambda execution role ARN
    Handler='health_check.lambda_handler',
    Code={
        'S3Bucket': 'cicdbotoakhil',
        'S3Key': 'lambda_functions/health_check.zip'  # Replace with the path to your Lambda code ZIP file
    },
    Timeout=30,
    Environment={
        'Variables': {
            'ALB_DNS': 'testwebapp-2133751168.ap-south-1.elb.amazonaws.com'  # Replace with your ALB DNS name
        }
    }
)
