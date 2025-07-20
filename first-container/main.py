from fastapi import FastAPI, HTTPException
import httpx
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="First Container - API Gateway")

# Get the second container URL from environment variable
SECOND_CONTAINER_URL = os.getenv("SECOND_CONTAINER_URL", "http://second-container:8001")

@app.get("/")
async def root():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{timestamp}] First Container: Received request to root endpoint")
    
    try:
        # Forward request to second container
        async with httpx.AsyncClient() as client:
            logger.info(f"[{timestamp}] First Container: Forwarding request to {SECOND_CONTAINER_URL}")
            response = await client.get(f"{SECOND_CONTAINER_URL}/")
            
            if response.status_code == 200:
                logger.info(f"[{timestamp}] First Container: Successfully received response from second container")
                return {"message": response.json()["message"], "forwarded_by": "first-container"}
            else:
                logger.error(f"[{timestamp}] First Container: Second container returned error: {response.status_code}")
                raise HTTPException(status_code=500, detail="Error from second container")
                
    except Exception as e:
        logger.error(f"[{timestamp}] First Container: Error forwarding request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/health")
async def health():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{timestamp}] First Container: Health check endpoint called")
    return {"status": "healthy", "container": "first-container"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 