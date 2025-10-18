import boto3
from gma_code.dao.parameter_store import get_parameter

def request_conversion(
        file_names: list[str],
        width: int,
        height: int,
        duration: int,
        loop: int,
        gif_name: str
):
    message_attributes = {
        'file_names': {
            'StringValue': str(file_names),
            'DataType': 'String'
            },
        'width': {
            'StringValue': str(width),
            'DataType': 'Number'
            }, 
        'height': {
            'StringValue': str(height),
            'DataType': 'Number'
            },
        'duration': {
            'StringValue': str(duration),
            'DataType': 'Number'
            }, 
        'loop': {
            'StringValue': str(loop),
            'DataType': 'Number'
            }
    }
    
    sqs = boto3.client('sqs', region_name=get_parameter("aws_region"))
    send_response = sqs.send_message(
        QueueUrl="https://sqs.ap-southeast-2.amazonaws.com/901444280953/a3-11",
        DelaySeconds=10,
        MessageBody=gif_name,
        MessageAttributes=message_attributes
    )
    return send_response["ResponseMetadata"]