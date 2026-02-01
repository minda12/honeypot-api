from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI(title="Agentic Honeypot API")

API_KEY = os.getenv("API_KEY", "my-secret-key")

class HoneypotRequest(BaseModel):
    message: str

@app.post("/honeypot/test")
def test_honeypot(
    payload: HoneypotRequest,
    x_api_key: str = Header(None)
):
    if x_api_key is None:
        raise HTTPException(status_code=401, detail="API key missing")

    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    return {
        "status": "ok",
        "scam_detected": True,
        "scam_type": "financial_phishing",
        "confidence_score": 0.85,
        "honeypot_engaged": True,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "extracted_intelligence": {
            "upi_ids": [],
            "bank_accounts": [],
            "phishing_links": []
        }
    }