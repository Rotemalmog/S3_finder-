import boto3
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError
import os


AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION")


def authenticate_to_aws(service_name, region=AWS_REGION, aws_access_key=AWS_ACCESS_KEY, aws_secret_key=AWS_SECRET_KEY):
    """
    Authenticate to AWS and return a service client.
    
    Parameters:
        service_name (str): The AWS service to interact with (e.g., 's3', 'ec2').
        region (str): The AWS region (default: 'us-east-1').
        aws_access_key (str): AWS Access Key ID (optional).
        aws_secret_key (str): AWS Secret Access Key (optional).
    
    Returns:
        client: The boto3 client for the specified AWS service.
    """
    try:
        if aws_access_key and aws_secret_key:
            # Authenticate using provided credentials
            session = boto3.session.Session(
                aws_access_key_id=aws_access_key,
                aws_secret_access_key=aws_secret_key,
                region_name=region
            )
        else:
            # Authenticate using default credentials (e.g., environment variables, ~/.aws/credentials)
            session = boto3.session.Session(region_name=region)
        
        # Create a client for the specified service
        client = session.client(service_name)
        print(f"Successfully authenticated to AWS for service: {service_name}")
        return client

    except NoCredentialsError:
        print("Error: No AWS credentials found. Please provide credentials or set them in the environment.")
    except PartialCredentialsError:
        print("Error: Incomplete AWS credentials provided.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return None

def file_exists_in_s3(client, bucket_name, file_name):
    """
    Checks if a file exists in an S3 bucket.

    Parameters:
        bucket_name (str): The name of the S3 bucket.
        file_name (str): The name of the file (object) in the S3 bucket.

    Returns:
        bool: True if the file exists, False otherwise.
    """

    try:
        # Try to get the metadata of the file (head_object returns metadata)
        client.head_object(Bucket=bucket_name, Key=file_name)
        return True  # File exists
    except ClientError as e:
        # If the error is a 404, file doesn't exist
        if e.response['Error']['Code'] == 'NoSuchKey':
            return False  # File does not exist
        else:
            # Other errors (e.g., permission issues)
            print(f"Error occurred: {e}")
            return False
        

def download_file_from_s3(client, bucket_name, file_name, download_path):
    """
    Downloads a file from an S3 bucket if it exists.

    Parameters:
        client: The authenticated boto3 client.
        bucket_name (str): The name of the S3 bucket.
        file_name (str): The name of the file (object) in the S3 bucket.
        download_path (str): The local path where the file will be saved.

    Returns:
        bool: True if the download was successful, False otherwise.
    """
    if file_exists_in_s3(client, bucket_name, file_name):
        try:
            # Download the file
            client.download_file(bucket_name, file_name, download_path)
            print(f"File '{file_name}' downloaded successfully to '{download_path}'.")
            # return True
        except ClientError as e:
            # Handle any errors during the download
            print(f"Error downloading file: {e}")
            return False
    else:
        print(f"File '{file_name}' does not exist in the bucket '{bucket_name}'.")
        return False

def generate_presigned_url(client, bucket_name, file_name, expiration=3600):
    """Generate a presigned URL to download the file from S3"""
    try:
        response = client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': file_name,
                'ResponseContentDisposition': f'attachment; filename="{file_name}"'  # Forces download
            },
            ExpiresIn=expiration
        )
    except NoCredentialsError:
        return None
    return response

def search_and_download_file(file_name):
    client = authenticate_to_aws("s3")
    bucket_name = "images_buket"

    if file_exists_in_s3(client ,bucket_name, file_name):
        print(f"File '{file_name}' exists in the bucket '{bucket_name}'.")
        url = generate_presigned_url(client ,bucket_name, file_name)
        return url
    else:
        print(f"File '{file_name}' does not exist in the bucket '{bucket_name}'.")
        return None
