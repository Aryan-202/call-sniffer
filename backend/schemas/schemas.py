from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    message: str

class ContactResponse(BaseModel):
    status: str
    message: str

class WebhookResponse(BaseModel):
    status: str
    message: str
    forward_status: Optional[str] = None
