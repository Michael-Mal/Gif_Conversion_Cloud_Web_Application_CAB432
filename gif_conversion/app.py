from gc_code.polling import begin_polling
from fastapi import FastAPI

app = FastAPI(title="GIF Conversion Microservice Health Check")

@app.get("/")
async def root():
    return {"message": "The GIF conversion microservice health check is successful."}

if __name__ == "__main__":
    import threading
    thread = threading.Thread(target=begin_polling, daemon=True)
    thread.start()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)