from fastapi import FastAPI
from gm_code.routes import v1_router, v2_router, v3_router

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

app.secret_key = '70495749971baffcf6634a5dcd0a782e2d538d7f5b7c1f81b251156319e213597037fd417c608827970a5b3f261e4b2f12923f20b5a2b2902694bfdf26988a97'

app.include_router(v1_router)
app.include_router(v2_router)
app.include_router(v3_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)