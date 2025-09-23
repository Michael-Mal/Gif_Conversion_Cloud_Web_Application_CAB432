import time
from gma_code.DynamoDB_DAO import *

debug = False
def start_garbage_collection(sleep: int = 30):
    while True:
        if debug: print("Sleep reset")
        if debug: print(read_all_images_data(ignore_restrictions=True))
        if debug: print(read_all_gif_data(ignore_restrictions=True))
        time.sleep(sleep)
        
