# Garbage Collection Module

import time
import gma_code.dao as dao
from botocore.exceptions import ClientError
import tempfile
from boto3 import client
from gma_code.dao.parameter_store import get_parameter

debug = False
time_until_old = 30 # Seconds
sqs = client('sqs', region_name=get_parameter("aws_region"))
queue_url = "https://sqs.ap-southeast-2.amazonaws.com/901444280953/a3-11-dlq"

def start_garbage_collection(sleep: int = 90):
    while True:
        current_time = int(time.time())

        if debug: print("Sleep reset\n" +
                        "images list: " + str(dao.dynamo_db.read_all_images(ignore_restrictions=True)) + 
                        "gif list: " + str(dao.dynamo_db.read_all_gif(ignore_restrictions=True)))

        # --- IMAGES ---
        for images in dao.dynamo_db.read_all_images(ignore_restrictions=True):
            # Filter images to only include images created over 30s ago to 
            # prevent deleting data that is still being processed
            if (int(images['time_created']['N']) < (current_time - time_until_old)):
                file_names = images['file_names']['L']
                # Try to access all of the files listed in the database
                try:
                    dao.s3.read_images(file_names=[file_name['S'] for file_name in file_names],
                                       width=0, height=0)
                except ClientError as e:
                    if e.response['Error']['Code'] == '404':
                        # File does not exist, delete references to the images
                        dao.s3.delete_images(file_names=[file_name['S'] for file_name in file_names])
                        dao.dynamo_db.delete_images(images['name']['S'][7:])
                        print("GarbageCollection: " + images['name']['S'] + " has been deleted due to a null file reference")
                        break

        # --- GIFS ---
        # Check the DLQ for gif conversions that have failed twice
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MessageAttributeNames=['All'],
            MaxNumberOfMessages = 1,
            VisibilityTimeout = 60
        )
        try:
            data = response['Messages'][0]
            gif_name = data['Body']
            dao.dynamo_db.delete_gif(gif_name)
            sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=data['ReceiptHandle']
                )
            print("GarbageCollection: " + gif_name + " has been deleted due to repeatedly failing conversion")

        except KeyError as e:
            # Nothing in DLQ
            pass
        
        time.sleep(sleep)
        
