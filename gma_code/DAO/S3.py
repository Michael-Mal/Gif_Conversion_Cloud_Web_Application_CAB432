import boto3
from fastapi import UploadFile
import tempfile
from PIL import Image

s3 = boto3.client('s3')

# --- IMAGES ---
# CREATE
def create_images(
        images: list[UploadFile],
        file_names: list[str]
):
    for image in images:
        s3.upload_fileobj(image.file, 'a2-11', file_names[images.index(image)])

# READ
def read_images(
        file_names: list[str],
        width: int,
        height: int
):
    """Returns images in list[Image.Image] format"""
    frames = []
    for file_name in file_names:
        with tempfile.TemporaryFile(mode="wb+") as image_dl:
            s3.download_fileobj('a2-11', file_name, image_dl)
            image = Image.open(image_dl)
            if not(width == 0) and not(height == 0):
                image = image.resize(size=(width, height))
            frames.append(image)
    return frames

# DELETE
def delete_images(
        file_names: list[str]
):
    images_keys = []
    for file_name in file_names:
        images_keys.append({'Key': file_name})
    s3.delete_objects(
        Bucket='a2-11',
        Delete={
            'Objects': images_keys
        }
    )

# --- GIFS ---
# CREATE
def create_gif(
        name: str,
        frames: list[Image.Image],
        duration: int,
        loop: int
):
    with tempfile.TemporaryFile(mode="w+b") as gif_upl:
        frames[0].save(gif_upl, format="GIF", append_images=frames, save_all=True, duration=duration, loop=loop)
        gif_upl.flush()
        gif_upl.seek(0)
        s3.upload_fileobj(gif_upl, 'a2-11', name + ".gif")

# READ
def read_gif(
        name: str,
        file
):
    """Returns gif in file format"""
    s3.download_fileobj('a2-11', name + ".gif", file)

# DELETE
def delete_gif(
        name: str
):
    key = name + ".gif"
    s3.delete_object(
        Bucket='a2-11',
        Key=key
    )