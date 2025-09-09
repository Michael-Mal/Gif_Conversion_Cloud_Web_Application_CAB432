# PLEASE READ
#
# For the submission, I decided not to include the images found in subdirectories (which are used to load down the API) to keep file sizes down
# If you would like to test it yourself, please add your own images into /Load_Images/ or /Hummingbird_Images/

import requests
import os

base_url = "http://localhost:3000"

def login(user: str):
    url = base_url + '/login/'

    json = {}
    if(user == "1"):
        json = {
            "username": 'michael',
            "password": 'mallett'
        }
    elif(user == "2"):
        json = {
            "username": 'test_account_1',
            "password": 'test_password'
        }
    

    response = requests.post(url, json=json)

    print("Status code: " + str(response.status_code) + "\nResponse: " + response.text)
    return response.text[14:-2]

#login()

def generate_headers(auth_token: str):
    if (auth_token == "1"):
        # Login as user 1
        auth_token = login("1")
    elif (auth_token == "2"):
        # Login as user 2
        auth_token = login("2")
    # Can also directly supply an auth token
    bearer_auth_token = "Bearer " + auth_token
    return {"Authorization": bearer_auth_token}




def upload_images(images, auth_token: str, name: str):
    url = base_url + '/v2/images/' + name + "/"

    headers = generate_headers(auth_token)

    data = {"public": False}

    response = requests.post(url, headers=headers, data=data, files=images)

    print("Status code: " + str(response.status_code) + "\nResponse: " + response.text)

def upload_test_images(auth_token: str):
    images = []
    image_dir = "./Hummingbird_Images/"
    for image in os.listdir(image_dir):
        image_path = image_dir + image
        images.append(("images", (image, open(image_path, "rb"))))
    upload_images(images, auth_token=auth_token, name="hummingbird_images")

upload_test_images("1")

def upload_load_images(auth_token: str):
    images = []
    image_dir = "./Load_Images/"
    for image in os.listdir(image_dir):
        image_path = image_dir + image
        images.append(("images", (image, open(image_path, "rb"))))
    upload_images(images, auth_token=auth_token, name="load_images")

upload_load_images("1")






def get_all_images(auth_token: str):
    url = base_url + '/v2/images/'
    headers = generate_headers(auth_token)
    data = {"public": False,
            "limit": 1,
            "page": 1}
    response = requests.get(url, headers=headers, data=data)
    print("Status code: " + str(response.status_code) + "\nResponse: " + response.text)

#get_all_images("1")




def convert_to_gif(auth_token: str, images_name: str, gif_name: str):
    url = base_url + '/v2/images/' + images_name + '/convert_to_gif/'

    data = {"gif_name": gif_name,
            "width": 280,
            "height": 280,
            "duration": 280,
            "loop": 2}

    headers = generate_headers(auth_token)

    response = requests.post(url, headers = headers, data = data)
    print("Status code: " + str(response.status_code) + "\nResponse: " + response.text)

#for i in range(100):
convert_to_gif("1", "michael_load_images", "load_gif")
convert_to_gif("1", "michael_hummingbird_images", "hummingbird_gif")



def get_all_gifs(auth_token: str, page: int, sort_descending = bool):
    url = base_url + '/v2/gifs/'
    headers = generate_headers(auth_token)
    data = {"public": False,
            "limit": 0,
            "page": page,
            "filter_by_images": "",
            "sort_by_field": "images_name",
            "sort_descending": sort_descending}
    response = requests.get(url, headers=headers, data=data)
    print("Status code: " + str(response.status_code) + "\nResponse: " + response.text)

get_all_gifs("1", 1, True)
#get_all_gifs("1", 1, False)



def download_gif(auth_token: str):
    url = base_url + '/v2/gifs/michael_test_gif/download/'

    headers = generate_headers(auth_token)

    response = requests.get(url, headers = headers)
    print("Status code: " + str(response.status_code) + "\nResponse: " + response.text)

#download_gif("1")




def upload_to_GIPHY(auth_token: str):
    url = base_url + '/v2/gifs/michael_test_gif/GIPHY/'

    headers = generate_headers(auth_token)    

    response = requests.post(url, headers = headers)
    print("Status code: " + str(response.status_code) + "\nResponse: " + response.text)

#upload_to_GIPHY("1")

def download_from_GIPHY(id: str):
    url = 'http://upload.giphy.com/v1/gifs'
    params = {"api_key": "ozIgfCZa4pYW1kO70WwBdgFPm0LfbJCu",
            "ids": id}
    response = requests.get(url, params=params)
    print("Status code: " + str(response.status_code) + "\nResponse: " + response.text)

#download_from_GIPHY("A5BKBHxIOKauFDBcaF")