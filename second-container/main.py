from fastapi import FastAPI
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Second Container - Backend API")

@app.get("/")
async def root():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{timestamp}] Second Container: Received request to root endpoint")
    return {"message": "hello from second api"}

@app.get("/health")
async def health():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{timestamp}] Second Container: Health check endpoint called")
    return {"status": "healthy", "container": "second-container"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
