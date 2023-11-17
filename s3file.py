import boto3

# Specify the region you want to use
region = 'ap-south-1'  # Replace with your desired AWS region, e.g., 'us-east-1'

# Initialize the S3 client with the specified region
s3 = boto3.client('s3', region_name=region)

# Create an S3 bucket
bucket_name = 'cicdbotoakhil'
location = {'LocationConstraint': region}

s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

