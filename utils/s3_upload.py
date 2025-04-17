import os

import boto3
from botocore.exceptions import NoCredentialsError

def upload_to_s3(file_path: str, bucket_name: str, object_key: str) -> bool:
    """
    Uploads a file to an S3 bucket.

    Args:
        file_path (str): Local path to the file.
        bucket_name (str): Name of the target S3 bucket.
        object_key (str): S3 object key (filename in bucket).

    Returns:
        bool: True if upload is successful, False otherwise.
    """
    try:
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION")
        )
        s3.upload_file(file_path, bucket_name, object_key)
        print(f"✅ File uploaded successfully to s3://{bucket_name}/{object_key}")
        return True
    except FileNotFoundError:
        print("❌ File not found:", file_path)
        return False
    except NoCredentialsError:
        print("❌ AWS credentials not found.")
        return False
    except Exception as e:
        print("❌ Upload failed:", str(e))
        return False
