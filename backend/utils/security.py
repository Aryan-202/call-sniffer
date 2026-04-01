import os
from fastapi import Header, HTTPException, status
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_SECRET_KEY = os.getenv("WEBHOOK_SECRET", "default_secret_do_not_use")

def verify_webhook_secret(x_webhook_secret: str = Header(..., alias="X-Webhook-Secret")):
    if x_webhook_secret != WEBHOOK_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid webhook secret"
        )
    return x_webhook_secret
