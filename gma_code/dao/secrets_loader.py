import boto3
import json
import os
from botocore.exceptions import ClientError

def get_secret(secret_name: str, region_name: str=None) -> dict:
    """
    Retrieve a secret from AWS Secret Manager
    Expects secret to be stored as JSON string.
    """
    region = "ap-southeast-2"
    client = boto3.client("secretsmanager", region_name=region)

    try:
        response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise RuntimeError(f"Failed to get secret {secret_name}: {e}")

    if "SecretString" in response:
        return json.loads(response["SecretString"])
    else:
        raise RuntimeError(f"Secret {secret_name} has no SecretString")
