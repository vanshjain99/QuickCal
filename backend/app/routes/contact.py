from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USERNAME")
    smtp_pass = os.getenv("SMTP_PASSWORD")

    # Set up email structures
    msg = MIMEMultipart()
    
    # Gmail Social Tab Classification Triggers:
    # 1. Precedence: list or Precedence: bulk
    # 2. List-ID: header to classify as list/social discussion
    # 3. List-Unsubscribe: header
    # 4. Subject prefix mimicking a social notification
    msg['From'] = f"calendarimport.com Social Hub <{smtp_user or 'noreply@calendarimport.com'}>"
    msg['To'] = receiver
    msg['Subject'] = f"[calendarimport.com Social Network] Support Inquiry from {payload.name}"
    msg['Precedence'] = 'list'
    msg['List-ID'] = '<social.calendarimport.com>'
    msg['List-Unsubscribe'] = '<mailto:unsubscribe@calendarimport.com?subject=unsubscribe>'

    body_text = (
        f"You received a new inquiry on calendarimport.com:\n\n"
        f"Name: {payload.name}\n"
        f"Email: {payload.email}\n\n"
        f"Message:\n{payload.message}"
    )
    msg.attach(MIMEText(body_text, 'plain'))

    # Local development logging
    print("\n--- NEW SUPPORT CONTACT INQUIRY ---")
    print(f"Recipient: {receiver}")
    print(f"Sender: {payload.name} ({payload.email})")
    print(f"Subject: {msg['Subject']}")
    print(f"Message:\n{payload.message}")
    print("------------------------------------\n")

    if not smtp_user or not smtp_pass:
        # If SMTP config is missing, return success since we logged to the console
        return {"status": "success", "message": "Inquiry logged to console (SMTP credentials missing)"}

    try:
        if smtp_port == 465:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port)
        else:
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()
        
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, receiver, msg.as_string())
        server.quit()
        return {"status": "success", "message": "Inquiry sent successfully"}
    except Exception as e:
        logger.error(f"SMTP sending failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
