import requests
import os
from gma_code import secrets_loader

API_HOST = os.getenv("ec2-54-206-89-132.ap-southeast-2.compute.amazonaws.com") # Change Public DNS when needed
API_PORT = os.getenv("API_PORT", "3000")
API_VER  = os.getenv("API_VER", "v3")

BASE_V3   = f"http://{API_HOST}:{API_PORT}/{API_VER}/"
BASE_AUTH = f"http://{API_HOST}:{API_PORT}/{API_VER}/auth/"

# Global variables to hold info when logged in to utilise script functions
user_1_auth = None
current_username = None


def api_signup(username: str, email: str, password: str):
    # Run once. Will 400 if the user already exists.
    url = BASE_AUTH + "signup"
    r = requests.post(url, json={"username": username, "email": email, "password": password})
    print("Signup:", r.status_code, r.text)
    return username, password

def api_confirm(username: str):
    code = input("Enter confirmation code: ")
    url = BASE_AUTH + "confirm"
    r = requests.post(url, json={"username": username, "code": code})
    print("Confirm:", r.status_code, r.text)

def api_login(username: str, password: str):
    # Returns tokens JSON: {id_token, access_token, refresh_token, ...}
    url = BASE_AUTH + "login"
    r = requests.post(url, json={"username": username, "password": password})
    print("Login:", r.status_code, r.text)
    return r.json() if r.ok else None

def auth_header_from_tokens(tokens: dict, use: str = "access"):
    if not tokens:
        return None
    authres = tokens.get("AuthenticationResult") or tokens  # handle both shapes
    if use == "access":
        token = authres.get("AccessToken") or authres.get("access_token")
    else:
        token = authres.get("IdToken") or authres.get("id_token")

    return {"Authorization": f"Bearer {token}"} if token else None

def upload_images(images, name: str):
    url = BASE_V3 + f"images/{name}"
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
    upload_images(images, name="hummingbird_images")

def upload_load_images():
    """Uploads the images in /Load_Images/, which are high-res and are used to load down the server."""
    images = []
    image_dir = "./Load_Images/"
    for image in os.listdir(image_dir):
        image_path = image_dir + image
        images.append(("images", (image, open(image_path, "rb"))))
    upload_images(images, name="load_images")

def get_all_images():
    url = BASE_V3 + 'images/'
    data = {"public": False,
            "limit": 1,
            "page": 1}
    response = requests.get(url, headers=user_1_auth, data=data)
    print("Status code: " + str(response.status_code) + "\nResponse: " + response.text)

def convert_to_gif(images_name: str, gif_name: str):
    url = BASE_V3 + 'images/' + images_name + '/convert_to_gif/'

    data = {"gif_name": gif_name,
            "width": 280,
            "height": 280,
            "duration": 280,
            "loop": 2}

    response = requests.post(url, headers = user_1_auth, data = data)
    print("Status code: " + str(response.status_code) + "\nResponse: " + response.text)

def get_all_gifs(page: int, sort_descending = bool):
    url = BASE_V3 + 'gifs/'
    data = {"public": False,
            "limit": 0,
            "page": page,
            "filter_by_images": "",
            "sort_by_field": "images_name",
            "sort_descending": sort_descending}
    response = requests.get(url, headers=user_1_auth, data=data)
    print("Status code: " + str(response.status_code) + "\nResponse: " + response.text)

def download_gif():
    url = BASE_V3 + 'gifs/michael_test_gif/download/'
    response = requests.get(url, headers = user_1_auth)
    print("Status code: " + str(response.status_code) + "\nResponse: " + response.text)

def upload_to_GIPHY():
    url = BASE_V3 + 'gifs/michael_hummingbird_gif/GIPHY/'
    response = requests.post(url, headers = user_1_auth)
    print("Status code: " + str(response.status_code) + "\nResponse: " + response.text)

def download_from_GIPHY(id: str):
    url = 'http://upload.giphy.com/v1/gifs'
    params = {"api_key": secrets_loader.get_secret("A2_Group11-GIPHY")["GIPHY_API"],
            "ids": id}
    response = requests.get(url, params=params)
    print("Status code: " + str(response.status_code) + "\nResponse: " + response.text)

#download_from_GIPHY("A5BKBHxIOKauFDBcaF")