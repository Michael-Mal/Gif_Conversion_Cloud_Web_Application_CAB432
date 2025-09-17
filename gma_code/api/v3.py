from fastapi import UploadFile, Form, HTTPException, Depends, Path
from fastapi.responses import JSONResponse, FileResponse
import os
import shutil
from PIL import Image
from typing import Optional
from gma_code.auth import authenticate_token
from gma_code.DynamoDB_DAO import *
import requests
import shutil
import boto3
import tempfile

s3 = boto3.client('s3')

async def upload_images(
    name: str,
    user = Depends(authenticate_token),
    images: list[UploadFile] = Form(...),
    public: Optional[bool] = Form(False)
):
    """Upload images to be processed

    Args:
        name (str): The name of the set of images to upload. All images must 
            be of the same filetype. If private, will be preceded by the username.
        user (str): The authentication token to use.
        images (list[UploadFile]): The image files to upload.
        images_type (str): The file types of the images.
        public (Optional[bool], optional): Specifies whether the images can be accessed by anyone or just this account. Defaults to False.

    Returns:
        list(str): If no exception occured: a success message including the names of the files that have been uploaded
    """

    #Add user to name if private
    if not(public):
        name = user['username'] + "_" + name

    check_exists(name, data_type="images", desired_outcome = False)

    # Generate the filenames
    file_type = images[0].filename.split(".")[1]
    file_names = []
    for i in range(len(images)):
        file_names.append(name + "_" + str(i) + "." + file_type)

    #Add to metadata
    create_images_data(name, user['username'], public, file_names)

    #Upload to S3
    success_msg = [name + " has been uploaded successfully"]
    for image in images:
        file_name = read_images_data(name)["file_names"]["L"][images.index(image)]["S"]
        s3.upload_fileobj(image.file, 'a2-11', file_name)
        success_msg.append(image.filename)

    return JSONResponse(status_code=201, content=success_msg)

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
    username = ""
    if not(public):
        # Only get user-made images
        username = user['username']
    data = read_all_images_data(username=username, limit=limit, page=page)
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
        HTTPException: If you are unauthorised to read data related to the 
            specified images of images don't exist

    Returns:
        dict: Metadata related to the images
    """
    check_exists(name, data_type="images")
    check_authorised(name, data_type="images", username=user['username'])
    return JSONResponse(content=read_images_data(name))

async def delete_images(
    name: str,
    user = Depends(authenticate_token)
):
    """Deletes a specific set of images

    Args:
        name (str): The name of the images.
        user (str): The authentication token to use.

    Raises:
        HTTPException: If you are unauthorised to delete the specified images,
            or the images don't exist

    Returns:
        str: Success response message
    """
    check_exists(name, data_type="images")
    check_authorised(name, data_type="images", username=user['username'])

    # Delete from S3
    images_keys = []
    for file_name in read_images_data(name)["file_names"]:
        images_keys.append({'Key': file_name})
    s3.delete_objects(
        Bucket='a2-11',
        Delete={
            'Objects': images_keys
        }
    )
    
    # Delete metadata
    delete_images_data(name)
    return JSONResponse(content=f"Successfully deleted {name}")

async def convert_to_gif(
    images_name: str,
    user = Depends(authenticate_token),
    gif_name: str = Form(...), 
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
    check_exists(images_name, data_type="images")
    check_authorised(images_name, data_type="images", username=user['username'])

    #Add user to name if private
    if not(public):
        gif_name = user['username'] + "_" + gif_name

    check_exists(gif_name, data_type="gif", desired_outcome=False)
    
    # Add to metadata
    create_gif_data(gif_name, user['username'], public, images_name, width, height, duration, loop)

    # Make gif
    frames = []
    for file_name in read_images_data(images_name)["file_names"]:
        with tempfile.TemporaryFile(mode="wb+") as image_dl:
            s3.download_fileobj('a2-11', file_name, image_dl)
            image = Image.open(image_dl)
            if not(width == 0) and not(height == 0):
                image = image.resize(size=(width, height))
            frames.append(image)

    # Save gif to S3
    with tempfile.TemporaryFile(mode="w+b") as gif_upl:
        frames[0].save(gif_upl, format="GIF", append_images=frames, save_all=True, duration=duration, loop=loop)
        gif_upl.flush()
        gif_upl.seek(0)
        s3.upload_fileobj(gif_upl, 'a2-11', gif_name + ".gif")

    return JSONResponse(status_code=201, content=f"Successfully converted {gif_name}")

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
    username = ""
    if not(public):
        # Only get user-made images
        username = user['username']
    data = read_all_gif_data(username=username, limit=limit, page=page, 
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
    check_exists(name, data_type="gif")
    check_authorised(name, data_type="gif", username=user['username'])
    return JSONResponse(content=read_gif_data(name))

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
    check_exists(name, data_type="gif")
    check_authorised(name, data_type="gif", username=user['username'])
    
    # Delete metadata
    delete_gif_data(name)

    # Delete from S3
    key = name + ".gif"
    s3.delete_object(
        Bucket='a2-11',
        Key=key
    )

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
    check_exists(name, data_type="gif")
    check_authorised(name, data_type="gif", username=user['username'])

    file_name = name + ".gif"

    increment_gif_downloads(name)

    # Download from s3
    with tempfile.NamedTemporaryFile(mode="w+b", delete=False) as gif_dl:
        s3.download_fileobj('a2-11', file_name, gif_dl)
        gif_dl.flush()
        gif_dl.seek(0)
        return FileResponse(gif_dl.name, filename=file_name, media_type='application/octet-stream')
        
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
    #check_exists(name, data_type="gif")
    #check_authorised(name, data_type="gif", username=user['username'])

    file_name = name + ".gif"

    url = 'http://upload.giphy.com/v1/gifs'

    data = {"api_key": "ozIgfCZa4pYW1kO70WwBdgFPm0LfbJCu",
                "country_code": country_code,
                "region": region}

    if not(tags == ""):
            data["tags"] = tags

    # Get file from S3
    with tempfile.TemporaryFile(mode="w+b") as gif_upl:
        s3.download_fileobj('a2-11', file_name, gif_upl)
        gif_upl.flush()
        gif_upl.seek(0)
        files = {"file": gif_upl}
    
        response = requests.post(url, data=data, files=files)
        if(response.status_code == 200):
            response_msg = {"Message": f"Successfully uploaded {name} to GIPHY",
                            "Detail": response.text}
            return JSONResponse(content=response_msg)
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Response: " + response.text)