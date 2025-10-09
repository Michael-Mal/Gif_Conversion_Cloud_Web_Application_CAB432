from fastapi import APIRouter
from gc_code.gif_conversion import convert_to_gif

router = APIRouter()

router.post("/images/{images_name}/convert_to_gif/")(convert_to_gif)