# This code has been repurposed from the Week 5 AWS Parameter Store Practical found at 
# https://canvas.qut.edu.au/courses/20367/pages/practical-aws-parameter-store-python?module_item_id=2064660
# , specifically the code that can be downloaded from https://canvas.qut.edu.au/courses/20367/files/6722624/download

import boto3
from botocore.exceptions import ClientError

parameter_prefix = "/a2/11/"
region = "ap-southeast-2" # Cannot get this from parameter store because this is needed for parameter store to work

ssm = boto3.client('ssm', region_name=region)

def get_parameter(name: str):
    try:
        return ssm.get_parameter(Name=parameter_prefix + name)['Parameter']['Value']
    except ClientError as e:
        raise RuntimeError(f"Failed to get parameter {name}: {e}")