from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database.database import get_db
from models.models import WebhookLog
from schemas.schemas import WebhookResponse
from utils.security import verify_webhook_secret
import logging

router = APIRouter(
    tags=["webhooks"]
)

logger = logging.getLogger("uvicorn.error")

@router.post("/webhook-test/call-leads", response_model=WebhookResponse)
async def handle_test_webhook(
    request: Request,
    db: Session = Depends(get_db),
    secret: str = Depends(verify_webhook_secret)
):
    payload = await request.json()
    logger.info(f"Received TEST Webhook payload: {payload}")
    
    db_log = WebhookLog(
        payload=payload,
        type="test"
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    
    return WebhookResponse(status="success", message="Test webhook recorded", id=db_log.id)

@router.post("/webhook/call-leads", response_model=WebhookResponse)
async def handle_prod_webhook(
    request: Request,
    db: Session = Depends(get_db),
    secret: str = Depends(verify_webhook_secret)
):
    payload = await request.json()
    logger.info(f"Received PROD Webhook payload: {payload}")
    
    db_log = WebhookLog(
        payload=payload,
        type="prod"
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    
    return WebhookResponse(status="success", message="Prod webhook recorded", id=db_log.id)
