from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database.database import get_db
from models.models import ContactMessage
from schemas.schemas import ContactCreate, ContactResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter(
    prefix="/contact",
    tags=["contact"]
)

limiter = Limiter(key_func=get_remote_address)

@router.post("/", response_model=ContactResponse)
@limiter.limit("5/minute")
def create_contact(request: Request, contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = ContactMessage(
        name=contact.name,
        email=contact.email,
        message=contact.message
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact
