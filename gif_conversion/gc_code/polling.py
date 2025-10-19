import boto3
import time
import gc_code.gif_conversion
import os
import ast

sqs = boto3.client('sqs', region_name='ap-southeast-2')
TEST_DLQ = os.getenv("TEST_DLQ", "false").lower() == "true"
queue_url = "https://sqs.ap-southeast-2.amazonaws.com/901444280953/a3-11"

def begin_polling():
    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MessageAttributeNames=['All'],
            MaxNumberOfMessages = 1,
            VisibilityTimeout = 60
        )
        
        try:
            data = response['Messages'][0]
            gif_name = data['Body']
            # If DLQ testing, simulate something going wrong (ie. nothing happens)
            if TEST_DLQ:
                print(f"Response received with no further action. (related to gif {gif_name})")
            else:
                data_att = data['MessageAttributes']
                file_names = ast.literal_eval(data_att['file_names']['StringValue'])
                width = int(data_att['width']['StringValue'])
                height = int(data_att['height']['StringValue'])
                duration = int(data_att['duration']['StringValue'])
                loop = int(data_att['loop']['StringValue'])

                gc_code.gif_conversion.convert_to_gif(
                    gif_name=gif_name,
                    file_names=file_names,
                    width=width,
                    height=height,
                    duration=duration,
                    loop=loop,
                )
                print(f"FINISHED POLL: Successfully converted {gif_name}")
                
                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=data['ReceiptHandle']
                )

        except KeyError as e:
            print(f"FINISHED POLL: No message in queue: {str(e)}")

        time.sleep(10)