from fastapi import APIRouter
from code.api import *
from code.auth import *

router = APIRouter()

# Connection
router.get("/")(conn_test)
router.post("/login/")(login)

# Images
router.post("/{ver}/images/{name}/")(upload_images)
router.get("/{ver}/images/")(get_all_images_data)
router.get("/{ver}/images/{name}/")(get_images_data)
router.delete("/{ver}/images/{name}/")(delete_images)
router.post("/{ver}/images/{images_name}/convert_to_gif/")(convert_to_gif)

# Gifs
router.get("/{ver}/gifs/")(get_all_gif_data)
router.get("/{ver}/gifs/{name}/")(get_gif_data)
router.delete("/{ver}/gifs/{name}/")(delete_gif)
router.get("/{ver}/gifs/{name}/download/")(download_gif)
router.post("/{ver}/gifs/{name}/GIPHY/")(upload_to_GIPHY)