import requests
import os

url_name = "localhost"
ver = "v3"
base_url = "http://" + url_name + ":3000/" + ver + "/"


def login(user: int):
    url = base_url + 'login/'

    json = {}
    if(user == 1):
        json = {
            "username": 'michael',
            "password": 'mallett'
        }
    elif(user == 2):
        json = {
            "username": 'test_account_1',
            "password": 'test_password'
        }
    

    response = requests.post(url, json=json)

    if(response.status_code == 200):
        bearer_auth_token = "Bearer " + response.text[14:-2]
        return {"Authorization": bearer_auth_token}
    else:
        print("wee waw wee waw " + response.text)

user_1_auth = login(1)
print("User 1 " + str(user_1_auth))

#user_2_auth = login(2)
#print("User 2 " + str(user_2_auth))




def upload_images(images, name: str):
    url = base_url + 'images/' + name + "/"
    data = {"public": False}
    response = requests.post(url, headers=user_1_auth, data=data, files=images)
    print("Status code: " + str(response.status_code) + "\nResponse: " + response.text)

def upload_test_images():
    """Uploads the images in /Hummingbird_Images/, which are low-res and easy to test with."""
    images = []
    image_dir = "./Hummingbird_Images/"
    for image in os.listdir(image_dir):
        image_path = image_dir + image
        images.append(("images", (image, open(image_path, "rb"))))
    upload_images(images, name="hummingbird")

upload_test_images()

def upload_load_images():
    """Uploads the images in /Load_Images/, which are high-res and are used to load down the server."""
    images = []
    image_dir = "./Load_Images/"
    for image in os.listdir(image_dir):
        image_path = image_dir + image
        images.append(("images", (image, open(image_path, "rb"))))
    upload_images(images, name="load")

#upload_load_images()




def get_all_images():
    url = base_url + 'images/'
    data = {"public": False,
            "limit": 1,
            "page": 1}
    response = requests.get(url, headers=user_1_auth, data=data)
    print("Status code: " + str(response.status_code) + "\nResponse: " + response.text)

#get_all_images()




def convert_to_gif(images_name: str, gif_name: str):
    url = base_url + 'images/' + images_name + '/convert_to_gif/'

    data = {"gif_name": gif_name,
            "width": 280,
            "height": 280,
            "duration": 280,
            "loop": 2}

    response = requests.post(url, headers = user_1_auth, data = data)
    print("Status code: " + str(response.status_code) + "\nResponse: " + response.text)

#convert_to_gif("michael_hummingbird", "hummingbird")

#for i in range(100):
#   convert_to_gif("michael_load", "load")





def get_all_gifs(page: int, sort_descending = bool):
    url = base_url + 'gifs/'
    data = {"public": False,
            "limit": 0,
            "page": page,
            "filter_by_images": "",
            "sort_by_field": "images_name",
            "sort_descending": sort_descending}
    response = requests.get(url, headers=user_1_auth, data=data)
    print("Status code: " + str(response.status_code) + "\nResponse: " + response.text)

#get_all_gifs(1, False)




def download_gif():
    url = base_url + 'gifs/michael_hummingbird/download/'
    response = requests.get(url, headers = user_1_auth)
    print("Status code: " + str(response.status_code) + "\nResponse: " + response.text)

#download_gif()




def upload_to_GIPHY():
    url = base_url + 'gifs/michael_hummingbird/GIPHY/'
    response = requests.post(url, headers = user_1_auth)
    print("Status code: " + str(response.status_code) + "\nResponse: " + response.text)

#upload_to_GIPHY()

def download_from_GIPHY(id: str):
    url = 'http://upload.giphy.com/v1/gifs'
    params = {"api_key": "ozIgfCZa4pYW1kO70WwBdgFPm0LfbJCu",
            "ids": id}
    response = requests.get(url, params=params)
    print("Status code: " + str(response.status_code) + "\nResponse: " + response.text)

#download_from_GIPHY("A5BKBHxIOKauFDBcaF")