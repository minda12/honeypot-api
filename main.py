from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI(title="Agentic Honeypot API")

API_KEY = os.getenv("API_KEY", "my-secret-key")

# ---------- Request Models ----------

class IncomingMessage(BaseModel):
    sender: str
    text: str
    timestamp: int

class HoneypotRequest(BaseModel):
    sessionId: str
    message: IncomingMessage
    conversationHistory: list
    metadata: dict

# ---------- Endpoint ----------

@app.post("/honeypot/test")
def honeypot_reply(
    payload: HoneypotRequest,
    x_api_key: str = Header(None)
):
    # 🔐 Auth
    if x_api_key is None:
        raise HTTPException(status_code=401, detail="API key missing")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

    scam_text = payload.message.text.lower()

    # 🧠 Minimal honeypot reply logic
    if "blocked" in scam_text or "suspended" in scam_text:
        reply = "Why is my account being suspended?"
    elif "verify" in scam_text:
        reply = "I am not sure how to verify, can you explain?"
    else:
        reply = "I don’t understand this message, please explain."

    return {
        "status": "success",
        "reply": reply
    }