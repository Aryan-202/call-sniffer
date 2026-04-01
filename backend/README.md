# 🚀 FastAPI Backend: Contact Form & Webhook System

A production-ready, highly-scalable backend for handling contact forms and incoming webhooks using FastAPI, SQLAlchemy, and SQLite.

## 🛠️ Features
- **POST /contact/**: Validated contact form submission with data storage.
- **POST /webhook-test/call-leads**: Secure testing endpoint for incoming webhooks.
- **POST /webhook/call-leads**: Production endpoint for external system integrations.
- **Security**: Custom header-based HMAC validation via `X-Webhook-Secret`.
- **Database**: ORM-powered storage with SQLite (upgradeable to PostgreSQL).
- **Logging**: Detailed logging for every incoming request and webhook payload.
- **Rate Limiting**: Basic middleware to prevent API abuse.

## 📁 Project Structure
```text
backend/
├── database/     # Database configuration & Session management
├── models/       # SQLAlchemy models (Database Tables)
├── routers/      # FastAPI API routes (Contact & Webhooks)
├── schemas/      # Pydantic schemas (Input/Output Validation)
├── utils/        # Security & helper utilities
├── main.py       # Application entry point
├── .env          # Private credentials (ignored by git)
└── requirements.txt
```

## ⚙️ Setup Instructions

### 1. Configure your Environment
Create a `.env` file in the root directory:
```env
DATABASE_URL=sqlite:///./database.db
WEBHOOK_SECRET=your_secret_key_here
```

### 2. Install Dependencies
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Server
```bash
uvicorn main:app --reload
```

## 🌐 Public Deployment (with Ngrok)
Expose your local server to the internet:
```bash
ngrok http 8000
```
This will provide you with a public URL like `https://xxxx-xxxx.ngrok-free.dev`. Use this for your external systems!

## 🧪 Testing with cURL
Send a test webhook:
```bash
curl -X POST "https://your-ngrok-url/webhook-test/call-leads" \
     -H "Content-Type: application/json" \
     -H "X-Webhook-Secret: your_secret_key_here" \
     -d '{"lead_id": 123, "status": "testing"}'
```

---
*Created with ❤️ by Antigravity AI*
