from fastapi import FastAPI
from gma_code.routes import v1_router, v2_router, v3_router
from gma_code.secrets_loader import get_secret

app = FastAPI(
    title="GIF Maker API",
    summary="Create gifs from images!",
    description="""Using GIF Maker API, you can now convert your images to gifs easily and efficiently.\n
                Features:\n
                - Upload images\n
                - Convert images to gifs\n
                - Retrieve data related to images and gifs\n
                - Download gifs or upload to GIPHY""",
    version="v3"
    )

jwt_secret = get_secret("A2_Group11-JWT_KEY")["JWT_SECRET"]
app.secret_key = jwt_secret

app.include_router(v1_router)
app.include_router(v2_router)
app.include_router(v3_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)