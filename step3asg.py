
import boto3
import os
# Initialize the Auto Scaling client
autoscaling = boto3.client('autoscaling')

# Create an Auto Scaling Launch Configuration
launch_config = autoscaling.create_launch_configuration(
    LaunchConfigurationName='web-app-launch-config-asgg',
    ImageId='ami-02a2af70a66af6dfb',  # Replace with your AMI ID
    InstanceType='t2.micro',  # Choose an appropriate instance type
    KeyName='boto3g5',  # Replace with your key pair name
    SecurityGroups=['sg-0da8749a6bea8d9d0'],
    UserData=f'''#!/bin/bash
                aws s3 cp s3://{'cicdbotoakhil'} /var/www/html/ --recursive
                systemctl enable apache2
                systemctl start apache2
             '''
)

# Create an Auto Scaling Group
autoscaling.create_auto_scaling_group(
    AutoScalingGroupName='web-app-asg',
    LaunchConfigurationName=launch_config['web-app-launch-config-asgg'],
    MinSize=1,
    MaxSize=5,
    VPCZoneIdentifier='subnet-xxxxxxxxxxxxxx,subnet-yyyyyyyyyyyyyy',  # Replace with your subnet IDs
    Tags=[{
        'Key': 'Name',
        'Value': 'web-app-instance',
        'PropagateAtLaunch': True
    }]
)

# Configure scaling policies based on metrics like CPU utilization or network traffic
autoscaling.put_scaling_policy(
    AutoScalingGroupName='web-app-asg',
    PolicyName='scale-out-policy',
    ScalingAdjustment=1,  # Increase desired capacity by 1
    Cooldown=300,  # 5 minutes cooldown
    AdjustmentType='ChangeInCapacity'
)

autoscaling.put_scaling_policy(
    AutoScalingGroupName='web-app-asg',
    PolicyName='scale-in-policy',
    ScalingAdjustment=-1,  # Decrease desired capacity by 1
    Cooldown=300,
    AdjustmentType='ChangeInCapacity'
)
