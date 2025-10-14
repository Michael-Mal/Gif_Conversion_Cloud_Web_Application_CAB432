import boto3
import tempfile
from PIL import Image

# Required to use boto3 - transferring data of type Image.Image through an API or SQS is impractical
s3 = boto3.client('s3')

def convert_to_gif(
        gif_name: str, 
        file_names: list[str],
        width: int,
        height: int,
        duration: int,
        loop: int
):
    frames = []
    for file_name in file_names:
        with tempfile.TemporaryFile(mode="wb+") as image_dl:
            s3.download_fileobj('a2-11', file_name, image_dl)
            image = Image.open(image_dl)
            if not(width == 0) and not(height == 0):
                image = image.resize(size=(width, height))
            frames.append(image)

    with tempfile.TemporaryFile(mode="w+b") as gif_upl:
        frames[0].save(gif_upl, format="GIF", append_images=frames, save_all=True, duration=duration, loop=loop)
        gif_upl.flush()
        gif_upl.seek(0)
        s3.upload_fileobj(gif_upl, 'a2-11', gif_name + ".gif")