from fastapi import UploadFile, Form, HTTPException, Depends, Path
from fastapi.responses import JSONResponse, FileResponse
import os
import shutil
from PIL import Image
from typing import Optional
from gma_code.auth import authenticate_token
from gma_code.dao.dynamo_db import *
import shutil

async def upload_images(
    name: str,
    images: list[UploadFile] = Form(...)
):
    """Upload images to be processed

    Args:
        name (str): The name of the set of images to upload. If private, will be preceded by the username.
        images (list[UploadFile]): The image files to upload.

    Returns:
        list(str): If no exception occured: a success message including the names of the files that have been uploaded
    """
    
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

    return JSONResponse(content=response_msg)

async def convert_to_gif(
    images_name: str,
    gif_name: Optional[str] = Form(""),
    width: Optional[int] = Form(0),
    height: Optional[int] = Form(0),
    duration: Optional[int] = Form(1000),
    loop: Optional[int] = Form(0)
):
    """Converts the specified images to a gif

    Args:
        images_name (str): The name of the images.
        gif_name (str): The name of the gif.
        width (Optional[int], optional): The width of the gif in pixels. Defaults to 0 (use image resolution instead).
        height (Optional[int], optional): The height of the gif in pixels. Defaults to 0 (use image resolution instead).
        duration (Optional[int], optional): The duration of the gif in milliseconds. Defaults to 1000 (1 second).
        loop (Optional[int], optional): How many times to loop the gif. Defaults to 0 (loop infinitely).

    Returns:
        str: Confirmation message if no exception is raised
    """

    #Check if path exists
    images_path = "uns_data/images/" + images_name
    
    
    if not(os.path.isdir(images_path)):
        raise HTTPException(status_code=400, detail=f"{images_name} does not exist")

    gif_name = images_name + "_w" + str(width) + "_h" + str(height) + "_d" + str(duration) + "_l" + str(loop) 
    
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

    return JSONResponse(content=f"Successfully converted {gif_name}")

async def download_gif(
    name: str,
):
    """Downloads a gif

    Args:
        name (str): The name of the gif.

    Returns:
        file: The specified gif in file form if no exception is raised
    """

    file_name = name + ".gif"
    file_path = "uns_data/gifs/" + file_name
        
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")  
    
    # Increment download
    gif_data[name]["downloads"] = gif_data[name]["downloads"] + 1
    
    return FileResponse(path=file_path, filename=file_name, media_type='application/octet-stream')
        