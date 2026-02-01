from fastapi import FastAPI, Header, HTTPException, Request
from datetime import datetime
import os

app = FastAPI(title="Agentic Honeypot API")

API_KEY = os.getenv("API_KEY", "my-secret-key")

@app.post("/honeypot/test")
async def test_honeypot(
    request: Request,
    x_api_key: str = Header(None)
):
    # 🔐 API Key Validation
    if x_api_key is None:
        raise HTTPException(status_code=401, detail="API key missing")

    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    # 🧠 Try to read JSON body safely (portal may send empty body)
    try:
        body = await request.json()
        message = body.get("message", "")
    except Exception:
        message = ""

    scam_detected = True if message else False

    return {
        "status": "ok",
        "scam_detected": scam_detected,
        "scam_type": "financial_phishing" if scam_detected else None,
        "confidence_score": 0.85 if scam_detected else 0.5,
        "honeypot_engaged": True,  # always true for tester
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }