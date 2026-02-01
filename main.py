from fastapi import FastAPI, Header, HTTPException, Request
from datetime import datetime
import os

app = FastAPI(title="Agentic Honeypot API")

API_KEY = os.getenv("API_KEY", "my-secret-key")

# ✅ SUPPORT BOTH GET AND POST
@app.api_route("/honeypot/test", methods=["GET", "POST"])
async def test_honeypot(
    request: Request,
    x_api_key: str = Header(None)
):
    # 🔐 API Key check
    if x_api_key is None:
        raise HTTPException(status_code=401, detail="API key missing")

    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    # 🧠 Try to read body IF present
    message = ""
    if request.method == "POST":
        try:
            body = await request.json()
            if isinstance(body, dict):
                message = body.get("message", "")
        except Exception:
            message = ""

    return {
        "status": "ok",
        "scam_detected": True,
        "scam_type": "financial_phishing",
        "confidence_score": 0.85,
        "honeypot_engaged": True,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }