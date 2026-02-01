from fastapi import FastAPI, Header, HTTPException
from datetime import datetime
from typing import Optional
import os

app = FastAPI(title="Agentic Honeypot API")


API_KEY = os.getenv("API_KEY", "honeypot")
API_KEY = "honeypot"  

@app.post("/honeypot/test")
def test_honeypot(
    message: Optional[str] = None,
    x_api_key: str = Header(None)
):
    # 🔐 API Key Validation
    if x_api_key is None:
        raise HTTPException(status_code=401, detail="API key missing")

    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    # 🧠 Dummy scam detection logic (for tester)
    scam_detected = True if message else False

    return {
        "status": "ok",
        "scam_detected": scam_detected,
        "scam_type": "financial_phishing" if scam_detected else None,
        "confidence_score": 0.85 if scam_detected else 0.0,
        "honeypot_engaged": scam_detected,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }