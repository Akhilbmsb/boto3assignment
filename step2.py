import boto3
import os

# Initialize the S3 client
s3 = boto3.client('s3')

# Use the existing S3 bucket
bucket_name = 'cicdbotoakhil'

# Clone the GitHub repository locally
os.system('git clone https://github.com/Akhilbmsb/TravelMemory.git')

# Navigate to the backend directory
os.chdir('TravelMemory/backend')

# Upload backend files to the S3 bucket
for root, dirs, files in os.walk('.'):
    for file in files:
        local_path = os.path.join(root, file)
        s3_path = os.path.relpath(local_path, '.')
        s3.upload_file(local_path, bucket_name, f'backend/{s3_path}')

# Navigate to the frontend directory
os.chdir('../frontend')

# Upload frontend files to the S3 bucket
for root, dirs, files in os.walk('.'):
    for file in files:
        local_path = os.path.join(root, file)
        s3_path = os.path.relpath(local_path, '.')
        s3.upload_file(local_path, bucket_name, f'frontend/{s3_path}')

# Use EC2 client to launch an instance
ec2 = boto3.client('ec2')

# Create a security group allowing inbound traffic on port 80 (HTTP)
security_group = ec2.create_security_group(
    GroupName='web-app-security-group',
    Description='Security group for the web application'
)
security_group_id = security_group['GroupId']

# Authorize inbound traffic on port 80
ec2.authorize_security_group_ingress(
    GroupId=security_group_id,
    IpPermissions=[{
        'IpProtocol': 'tcp',
        'FromPort': 80,
        'ToPort': 80,
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    }]
)

# Launch an EC2 instance
instance = ec2.run_instances(
    ImageId='ami-02a2af70a66af6dfb',  # Replace with your AMI ID
    InstanceType='t2.micro',  # Choose an appropriate instance type
    KeyName='boto3g5',  # Replace with your key pair name
    MinCount=1,
    MaxCount=1,
    SecurityGroupIds=[security_group_id],
    UserData=f'''#!/bin/bash
                aws s3 cp s3://{bucket_name} /var/www/html/ --recursive
                systemctl enable apache2
                systemctl start apache2
             '''
)['Instances'][0]

# Wait for the instance to be running
ec2.get_waiter('instance_running').wait(InstanceIds=[instance['InstanceId']])
print(f"Web application deployed. Instance ID: {instance['InstanceId']}")
