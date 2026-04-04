from fastapi import APIRouter, Request
from schemas.schemas import ContactCreate, ContactResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging

router = APIRouter(
    prefix="/contact",
    tags=["contact"]
)

logger = logging.getLogger("uvicorn.error")
limiter = Limiter(key_func=get_remote_address)

@router.post("/", response_model=ContactResponse)
@limiter.limit("5/minute")
async def create_contact(request: Request, contact: ContactCreate):
    # Log incoming contact form data to your terminal
    logger.info(f"📬 NEW CONTACT SUBMISSION:")
    logger.info(f"Name: {contact.name}")
    logger.info(f"Email: {contact.email}")
    logger.info(f"Message: {contact.message}")
    
    return ContactResponse(status="success", message="Contact data received and logged locally.")
