from fastapi import APIRouter, Depends, Request
from schemas.schemas import WebhookResponse
from utils.security import verify_webhook_secret
import logging
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

# THE TEAMMATE'S URL FROM YOUR REQUEST
TEST_NGROK_FORWARD_URL = "https://vitalistically-recherch-charley.ngrok-free.dev/webhook-test/call-leads"

router = APIRouter(
    tags=["webhooks"]
)

logger = logging.getLogger("uvicorn.error")

@router.post("/webhook-test/call-leads", response_model=WebhookResponse)
async def handle_test_webhook(
    request: Request,
    secret: str = Depends(verify_webhook_secret)
):
    # 1. READ INCOMING JSON DATA 
    payload = await request.json()
    logger.info(f"🔔 Received Incoming Webhook for FORWARDING: {payload}")
    
    # 2. IMMEDIATELY FORWARD TO THE EXTERNAL TEST URL
    forward_status = "unattempted"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                TEST_NGROK_FORWARD_URL, 
                json=payload,
                headers={"X-Webhook-Secret": secret} # Use the same secret for forwarding
            )
            forward_status = f"success_{response.status_code}"
            logger.info(f"🚀 Forwarded payload to Teammate URL. Status: {response.status_code}")
    except Exception as e:
        forward_status = "failed"
        logger.error(f"❌ Failed to forward payload: {str(e)}")
    
    return WebhookResponse(
        status="received", 
        message="Payload processed professionally", 
        forward_status=forward_status
    )

@router.post("/webhook/call-leads", response_model=WebhookResponse)
async def handle_prod_webhook(
    request: Request,
    secret: str = Depends(verify_webhook_secret)
):
    # For production, we just log and return (you can add production forwarding here later)
    payload = await request.json()
    logger.info(f"🔔 Received PROD Webhook payload: {payload}")
    
    return WebhookResponse(status="success", message="Production webhook logged in terminal")
