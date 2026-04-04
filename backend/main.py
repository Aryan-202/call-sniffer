import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from routers import contact, webhook

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# STARTING THE APP 
app = FastAPI(
    title="Contact & Webhook FORWARDER API",
    description="Backend system for production-ready contact forms and webhook forwarding",
    version="1.0.0"
)

# NO MORE DATABASE TABLE CREATION NEEDED! 

# Rate Limiting setup 
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# CORS (To connect with your React Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open to all origins for your React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Standard Request Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

# Include our modified Routers
app.include_router(contact.router)
app.include_router(webhook.router)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "API Forwarder is active"}
