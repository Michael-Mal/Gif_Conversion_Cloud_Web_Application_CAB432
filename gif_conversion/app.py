from fastapi import FastAPI
from gc_code.routes import router

app = FastAPI(
    title="GIF Maker API - Conversion",
    summary="Convert images to gifs!"
    )

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)