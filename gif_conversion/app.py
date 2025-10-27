from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="GIF Conversion Microservice Health Check")

@app.get("/")
async def root():
    return JSONResponse(status_code=200, content="Health check successful")

if __name__ == "__main__":
    from gc_code.polling import begin_polling
    begin_polling()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)