# Garbage Collection Module

import time
import gma_code.DAO as DAO
from botocore.exceptions import ClientError
import tempfile

debug = False
time_until_old = 30 # Seconds

def start_garbage_collection(sleep: int = 60):
    while True:
        current_time = int(time.time())

        if debug: print("Sleep reset\n" +
                        "images list: " + str(DAO.DynamoDB.read_all_images(ignore_restrictions=True)) + 
                        "gif list: " + str(DAO.DynamoDB.read_all_gif(ignore_restrictions=True)))

        # --- IMAGES ---
        for images in DAO.DynamoDB.read_all_images(ignore_restrictions=True):
            # Filter images to only include images created over 30s ago to 
            # prevent deleting data that is still being processed
            if (int(images['time_created']['N']) < (current_time - time_until_old)):
                file_names = images['file_names']['L']
                # Try to access all of the files listed in the database
                try:
                    DAO.S3.read_images(file_names=[file_name['S'] for file_name in file_names],
                                       width=0, height=0)
                except ClientError as e:
                    if e.response['Error']['Code'] == '404':
                        # File does not exist, delete references to the images
                        DAO.S3.delete_images(file_names=[file_name['S'] for file_name in file_names])
                        DAO.DynamoDB.delete_images(images['name']['S'][7:])
                        print("GarbageCollection: " + images['name']['S'] + " has been deleted due to a null file reference")
                        break

        # --- GIFS ---
        for gif in DAO.DynamoDB.read_all_gif(ignore_restrictions=True):
            # Filter gifs to only include gifs created over 30s ago as per above
            if (int(gif['time_created']['N']) < (current_time - time_until_old)):
                gif_name = gif['name']['S'][4:]
                try:
                    with tempfile.TemporaryFile(mode="w+b") as gif_dl:
                        DAO.S3.read_gif(gif_name, gif_dl)
                except ClientError as e:
                    if e.response['Error']['Code'] == '404':
                        # File does not exist, delete references to the gif
                        DAO.DynamoDB.delete_gif(gif_name)
                        print("GarbageCollection: " + gif_name + " has been deleted due to a null file reference")
                        break
        
        time.sleep(sleep)
        
