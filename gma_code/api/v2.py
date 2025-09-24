from fastapi import UploadFile, Form, HTTPException, Depends, Path
from fastapi.responses import JSONResponse, FileResponse
from gma_code.secrets_loader import get_secret
import os
import shutil
from PIL import Image
from typing import Optional
from gma_code.auth import authenticate_token
from gma_code.DAO.DynamoDB import *
import requests
import shutil


async def upload_images(
    name: str,
    user = Depends(authenticate_token),
    images: list[UploadFile] = Form(...),
    public: Optional[bool] = Form(False)
):
    """Upload images to be processed

    Args:
        name (str): The name of the set of images to upload. If private, will be preceded by the username.
        user (str): The authentication token to use.
        images (list[UploadFile]): The image files to upload.
        public (Optional[bool], optional): Specifies whether the images can be accessed by anyone or just this account. Defaults to False.

    Returns:
        list(str): If no exception occured: a success message including the names of the files that have been uploaded
    """

    
    #Add user to name if private
    if not(public):
        name = user['username'] + "_" + name

    
    #Make images directory
    if not(os.path.exists("uns_data/")):
        os.mkdir("uns_data/")
    if not(os.path.exists("uns_data/images/")):
        os.mkdir("uns_data/images/")
    path = "./uns_data/images/" + name
    try:
        os.makedirs(path, exist_ok=False)
    except OSError as e:
        raise HTTPException(status_code=400, detail=f"Name already exists: {e}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid directory: {e}")

    response_msg = [name + " has been uploaded successfully"]

    for image in images:

        #Save images to directory
        file_path = os.path.join(path, image.filename)
        try:
            with open(file_path, "wb") as f:
                shutil.copyfileobj(image.file, f)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save {image.filename}: {e}")
        
        response_msg.append(image.filename)

    #Add to metadata
    create_images(name, user['username'], public)

    return JSONResponse(content=response_msg)

async def get_all_images_data(
    user = Depends(authenticate_token),
    public: Optional[bool] = Form(False),
    limit: Optional[int] = Form(0),
    page: Optional[int] = Form(1)
):
    """Retrieves the metadata related to images that are either public or belong to you

    Args:
        user (str): The authentication token to use.
        public (Optional[bool], optional): Specifies whether you want to 
            retrieve images that are public or belong to you. Defaults to False (belong to you).
        limit (Optional[int], optional): Specifies if you want to limit the results. Defaults to 0 (no limit).
        page (Optional[int], optional): If the results are limited, specify which page of results to access. Defaults to 1.

    Returns:
        dict: Metadata related to the images
    """
    data = read_all_images(user['username'], public=public, limit=limit, page=page)
    return JSONResponse(content=data)

async def get_images_data(
    name: str,
    user = Depends(authenticate_token),
):
    """Retrieves the metadata related to a specific set of images

    Args:
        name (str): The name of the images.
        user (str): The authentication token to use.

    Raises:
        HTTPException: If you are unauthorised to read data related to the specified images

    Returns:
        dict: Metadata related to the images
    """
    if not(check_authorised(name, "images", user['username'])):
        raise HTTPException(status_code=403, detail=f"You are unauthorised to read data related to {name}")

    return JSONResponse(content=read_images(name))

async def delete_images(
    name: str,
    user = Depends(authenticate_token)
):
    """Deletes a specific set of images

    Args:
        name (str): The name of the images.
        user (str): The authentication token to use.

    Raises:
        HTTPException: If you are unauthorised to delete the specified images

    Returns:
        str: Success response message
    """

    if not(check_authorised(name, "images", user['username'])):
        raise HTTPException(status_code=403, detail=f"You are unauthorised to delete {name}")

    shutil.rmtree("uns_data/images/" + name)
    delete_images(name)

    return JSONResponse(content=f"Successfully deleted {name}")

async def convert_to_gif(
    images_name: str,
    user = Depends(authenticate_token),
    gif_name: Optional[str] = Form(""),
    width: Optional[int] = Form(0),
    height: Optional[int] = Form(0),
    duration: Optional[int] = Form(1000),
    loop: Optional[int] = Form(0),
    public: Optional[bool] = Form(False)
):
    """Converts the specified images to a gif

    Args:
        images_name (str): The name of the images.
        user (str): The authentication token to use.
        gif_name (str): The name of the gif (will be preceded by username if private).
        width (Optional[int], optional): The width of the gif in pixels. Defaults to 0 (use image resolution instead).
        height (Optional[int], optional): The height of the gif in pixels. Defaults to 0 (use image resolution instead).
        duration (Optional[int], optional): The duration of the gif in milliseconds. Defaults to 1000 (1 second).
        loop (Optional[int], optional): How many times to loop the gif. Defaults to 0 (loop infinitely).
        public (Optional[bool], optional): Specifies whether the gif can be accessed by anyone or just this account. Defaults to False.

    Returns:
        str: Confirmation message if no exception is raised
    """
 
    #Check if path exists
    images_path = "uns_data/images/" + images_name
    
    
    try:
        read_images(images_name)
    except KeyError:
            raise HTTPException(status_code=400, detail=f"{images_name} does not exist")

    #Check if user is authorised
    if not(check_authorised(images_name, "images", user['username'])):
        raise HTTPException(status_code=403, detail=f"You are unauthorised to convert {images_name}")

    #Add user to name if private
    if not(public):
        gif_name = user['username'] + "_" + gif_name
    
    #Make gifs directory
    if not(os.path.exists("uns_data/gifs/")):
        os.mkdir("uns_data/gifs/")
    gif_file_path = "uns_data/gifs/" + gif_name + ".gif"
    
    #Make gif
    image_paths = [images_path + "/" + file_name for file_name in os.listdir(images_path)]
    frames = []
    for image in image_paths:
        opened_image = Image.open(image)
        if not(width == 0) and not(height == 0):
            opened_image = opened_image.resize(size=(width, height))
        frames.append(opened_image)
    frame_one = frames[0]
    frame_one.save(gif_file_path, format="GIF", append_images=frames, save_all=True, duration=duration, loop=loop)
    
    #Add to metadata
    create_gif(gif_name, user['username'], public, images_name, width, height, duration, loop)

    return JSONResponse(content=f"Successfully converted {gif_name}")

async def get_all_gif_data(
    user = Depends(authenticate_token),
    public: Optional[bool] = Form(False),
    limit: Optional[int] = Form(0),
    page: Optional[int] = Form(1),
    filter_by_images: Optional[str] = Form(""),
    sort_by_field: Optional[str] = Form(""),
    sort_descending: Optional[bool] = Form(False)
):
    """Retrieves the metadata related to gifs that are either public or belong to you

    Args:
        user (str): The authentication token to use.
        public (Optional[bool], optional): Specifies whether you want to 
            retrieve gifs that are public or belong to you. Defaults to False (belong to you).
        limit (Optional[int], optional): Specifies if you want to limit the results. Defaults to 0 (no limit).
        page (Optional[int], optional): If the results are limited, specify which page of results to access. Defaults to 1.
        filter_by_images (Optional[str], optional): Specifies if you want to 
            filter the results by the images that were used to create the gif. Defaults to "" (no filter).
        sort_by_field (Optional[str], optional): Specifies if the results will be sorted by a specific field. Defaults to "" (no sort).
        sort_descending (Optional[bool], optional): Specifies if the sort will be in descending order instead of ascending. Defaults to False.

    Returns:
        dict: Metadata related to the gifs
    """
    data = read_all_gif(user['username'], public=public, limit=limit, page=page, 
                             filter_by_images=filter_by_images, sort_by_field=sort_by_field,
                             sort_descending=sort_descending)
    return JSONResponse(content=data)

async def get_gif_data(
    name: str,
    user = Depends(authenticate_token),
):
    """Retrieves the metadata related to a specific gif

    Args:
        name (str): The name of the gif.
        user (str): The authentication token to use.

    Raises:
        HTTPException: If you are unauthorised to read data related to the specified gif

    Returns:
        dict: Metadata related to the gif
    """
    if not(check_authorised(name, "gif", user['username'])):
        raise HTTPException(status_code=403, detail=f"You are unauthorised to read data related to {name}")

    return JSONResponse(content=read_gif(name))

async def delete_gif(
    name: str,
    user = Depends(authenticate_token)
):
    """Deletes a specific gif

    Args:
        name (str): The name of the gif.
        user (str): The authentication token to use.

    Raises:
        HTTPException: If you are unauthorised to delete the specified gif

    Returns:
        str: Success response message
    """
    if not(check_authorised(name, "gif", user['username'])):
        raise HTTPException(status_code=403, detail=f"You are unauthorised to delete {name}")

    os.remove("uns_data/gifs/" + name + ".gif")
    delete_gif(name)

    return JSONResponse(content=f"Successfully deleted {name}")

async def download_gif(
    name: str,
    user = Depends(authenticate_token)
):
    """Downloads a gif

    Args:
        name (str): The name of the gif.
        user (str): The authentication token to use.

    Returns:
        file: The specified gif in file form if no exception is raised
    """

    file_name = name + ".gif"
    file_path = "uns_data/gifs/" + file_name

    try:
        read_gif(name)
    except KeyError:
        raise HTTPException(status_code=400, detail=f"{name} does not exist")
    
    #Check if user is authorised
    if not(check_authorised(name, "gif", user["username"])):
            raise HTTPException(status_code=403, detail=f"You are unauthorised to download {name}") 
    
    # Increment download
    gif_data[name]["downloads"] = gif_data[name]["downloads"] + 1
    
    return FileResponse(path=file_path, filename=file_name, media_type='application/octet-stream')
        
async def upload_to_GIPHY(
    name: str,
    user = Depends(authenticate_token),
    tags: Optional[str] = Form(""),
    country_code: Optional[str] = Form("AU"),
    region: Optional[str] = Form("QLD")
):
    """Uploads a gif to GIPHY

    Args:
        name (str): The name of the gif.
        user (str): The authentication token to use.
        tags (Optional[str], optional): Tags to add to your gif. Defaults to "" (no tags).
        country_code (Optional[str], optional): Your country code. Defaults to "AU".
        region (Optional[str], optional): Your region code. Defaults to "QLD".

    Returns:
        dict: The response message from GIPHY if authorised
    """

    giphy_api_key = get_secret("A2_Group11-GIPHY")["GIPHY_API"]

    #Check if user is authorised
    if not(check_authorised(name, "gif", user["username"])):
            raise HTTPException(status_code=403, detail=f"You are unauthorised to upload {name}")

    file_name = name + ".gif"
    file_path = "uns_data/gifs/" + file_name

    url = 'http://upload.giphy.com/v1/gifs'

    with open(file_path, "rb") as f:

        data = {"api_key": giphy_api_key,
                "country_code": country_code,
                "region": region}
        files = {"file": f}
        if not(tags == ""):
            data["tags"] = tags
    
        response = requests.post(url, data=data, files=files)
        #print("Status code: " + str(response.status_code) + "\nResponse: " + response.text)
        if(response.status_code == 200):
            response_msg = {"Message": f"Successfully uploaded {name} to GIPHY",
                            "Detail": response.text}
            return JSONResponse(content=response_msg)
        else:
            raise HTTPException(status_code=400, detail=f"Status code: " + str(response.status_code) + "\nResponse: " + response.text)