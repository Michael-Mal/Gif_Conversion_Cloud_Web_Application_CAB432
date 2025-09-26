from fastapi import APIRouter
import gma_code.api.v1 as v1
import gma_code.api.v2 as v2
import gma_code.api.v3 as v3
import gma_code.auth as auth
import gma_code.mfa_auth as mfa_auth

# --- Version 1 ---
v1_router = APIRouter(prefix="/v1")

v1_router.post("/images/{name}/")(v1.upload_images)
v1_router.post("/images/{images_name}/convert_to_gif/")(v1.convert_to_gif)
v1_router.get("/gifs/{name}/download/")(v1.download_gif)


# --- Version 2 ---
v2_router = APIRouter(prefix="/v2")

v2_router.post("/auth/signup")(auth.signup)
v2_router.post("/auth/confirm")(auth.confirm_user)
v2_router.post("/auth/login")(auth.authenticate)

# Images
v2_router.post("/images/{name}/")(v2.upload_images)
v2_router.get("/images/")(v2.get_all_images_data)
v2_router.get("/images/{name}/")(v2.get_images_data)
v2_router.delete("/images/{name}/")(v2.delete_images)
v2_router.post("/images/{images_name}/convert_to_gif/")(v2.convert_to_gif)

# Gifs
v2_router.get("/gifs/")(v2.get_all_gif_data)
v2_router.get("/gifs/{name}/")(v2.get_gif_data)
v2_router.delete("/gifs/{name}/")(v2.delete_gif)
v2_router.get("/gifs/{name}/download/")(v2.download_gif)
v2_router.post("/gifs/{name}/GIPHY/")(v2.upload_to_GIPHY)


# --- Version 3 ---
v3_router = APIRouter(prefix="/v3")


v3_router.post("/auth/signup")(auth.signup)
v3_router.post("/auth/confirm")(auth.confirm_user)
v3_router.post("/auth/login")(auth.authenticate)

v3_router.post("/auth/mfa/associate")(mfa_auth.associate_totp)
v3_router.post("/auth/mfa/verify")(mfa_auth.verify_totp)
v3_router.post("/auth/mfa/set-preferred")(mfa_auth.set_totp_preferred)

# Images
v3_router.post("/images/{name}/")(v3.upload_images)
v3_router.get("/images/")(v3.get_all_images_data)
v3_router.get("/images/{name}/")(v3.get_images_data)
v3_router.delete("/images/{name}/")(v3.delete_images)
v3_router.post("/images/{images_name}/convert_to_gif/")(v3.convert_to_gif)

# Gifs
v3_router.get("/gifs/")(v3.get_all_gif_data)
v3_router.get("/gifs/{name}/")(v3.get_gif_data)
v3_router.delete("/gifs/{name}/")(v3.delete_gif)
v3_router.get("/gifs/{name}/download/")(v3.download_gif)
v3_router.post("/gifs/{name}/GIPHY/")(v3.upload_to_GIPHY)