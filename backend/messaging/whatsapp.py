import requests
import logging
import os

logger = logging.getLogger(__name__)

# Constants (In production, load these from environment variables)
WHATSAPP_API_URL = "https://graph.facebook.com/v17.0"
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_ID", "dummy_id")
ACCESS_TOKEN = os.getenv("WHATSAPP_TOKEN", "dummy_token")

def send_message(to_number: str, text_body: str):
    """
    Sends a WhatsApp text message using the Cloud API.
    """
    url = f"{WHATSAPP_API_URL}/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": text_body},
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send WhatsApp message: {e}")
        if e.response:
             logger.error(f"Response: {e.response.text}")
        return None
