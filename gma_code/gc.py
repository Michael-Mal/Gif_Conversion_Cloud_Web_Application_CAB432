# Garbage Collection Module

import time
import gma_code.DAO as DAO

debug = False
def start_garbage_collection(sleep: int = 30):
    while True:
        if debug: print("Sleep reset")

        if debug: print("images list: " + str(DAO.DynamoDB.read_all_images(ignore_restrictions=True)))
        if debug: print("gif list: " + str(DAO.DynamoDB.read_all_gif(ignore_restrictions=True)))

        for images in DAO.DynamoDB.read_all_images(ignore_restrictions=True):
            # Filter images to only include images created over a minute ago to 
            # prevent deleting data that is still being processed
            if (int(images['time_created']['N']) < (int(time.time()) - 60)):
                number_of_files = len(images['file_names']['L'])
                # TODO: Get the number of files from S3
                    

        for gif in DAO.DynamoDB.read_all_gif(ignore_restrictions=True):
            # Filter gifs to only include gifs created over a minute ago as per above
            if (int(gif['time_created']['N']) < (int(time.time()) - 60)):
                pass
                #old_file_names.append(gif['name']['S'] + ".gif")
        
        time.sleep(sleep)
        
