from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import urllib.request
import urllib.error
import json
import logging

router = APIRouter(prefix="/api/v1", tags=["Contact"])
logger = logging.getLogger(__name__)

class ContactRequest(BaseModel):
    name: str
    email: str
    message: str

@router.post("/contact")
async def handle_contact_form(payload: ContactRequest):
    # Retrieve the receiver email from .env
    receiver = os.getenv("CONTACT_RECEIVER_EMAIL")
    if not receiver:
        logger.error("CONTACT_RECEIVER_EMAIL environment variable is not configured.")
        raise HTTPException(
            status_code=500,
            detail="Contact submission service is not configured on the server."
        )

    resend_api_key = os.getenv("RESEND_API_KEY")

    # Local development logging
    print("\n--- NEW SUPPORT CONTACT INQUIRY ---")
    print(f"Recipient: {receiver}")
    print(f"Sender: {payload.name} ({payload.email})")
    print(f"Message:\n{payload.message}")
    print("------------------------------------\n")

    if not resend_api_key:
        # If Resend API Key is missing, return success since we logged to the console
        return {"status": "success", "message": "Inquiry logged to console (RESEND_API_KEY missing)"}

    # Format email fields for Resend API
    # Free tier uses onboarding@resend.dev as verified sender
    resend_payload = {
        "from": f"QuickCal Support <onboarding@resend.dev>",
        "to": [receiver],
        "reply_to": payload.email,
        "subject": f"QuickCal Support Inquiry: {payload.name}",
        "text": (
            f"You received a new inquiry on QuickCal:\n\n"
            f"Name: {payload.name}\n"
            f"Email: {payload.email}\n\n"
            f"Message:\n{payload.message}"
        )
    }

    try:
        req = urllib.request.Request(
            "https://api.resend.com/emails",
            data=json.dumps(resend_payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {resend_api_key}",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        
        # Set a 10-second timeout to prevent requests from hanging
        with urllib.request.urlopen(req, timeout=10.0) as response:
            response_data = json.loads(response.read().decode("utf-8"))
            logger.info(f"Resend email sent: {response_data}")
            return {"status": "success", "message": "Inquiry sent successfully"}
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        logger.error(f"Resend API HTTP Error {e.code}: {error_body}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send email via Resend API: {error_body}"
        )
    except Exception as e:
        logger.error(f"Resend API connection failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to connect to Resend API: {str(e)}"
        )
