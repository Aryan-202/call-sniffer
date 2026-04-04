from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get webhook URL from .env (default to production, can switch based on need)
# The user provided both test and production. Let's use production for now or add logic to switch.
WEBHOOK_URL = os.getenv("WEBHOOK_PRODUCTION_URL")

app = FastAPI(title="Form Submission Server")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FormData(BaseModel):
    name: str
    phone: str
    email: EmailStr
    type: str
    message: str

@app.post("/submit")
async def submit_form(data: FormData):
    if not WEBHOOK_URL:
        raise HTTPException(status_code=500, detail="Webhook URL not configured")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(WEBHOOK_URL, json=data.dict())
            
            if response.status_code >= 400:
                raise HTTPException(
                    status_code=response.status_code, 
                    detail=f"n8n webhook returned an error: {response.text}"
                )
            
            return {"status": "success", "message": "Form data sent to n8n"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
