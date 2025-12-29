from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from rafeeq import users, dispatcher
from datetime import datetime

router = APIRouter(prefix="/rafeeq", tags=["Rafeeq"])

from typing import Dict, Any

# Data Models
class OptInRequest(BaseModel):
    phone_number: str
    name: str = "User"
    timezone: str = "UTC"
    latitude: float
    longitude: float
    preferences: Dict[str, Any] = {} # {prayers: [], method: 'text', intensity: 'steady'}

class MessagePayload(BaseModel):
    # Simplified webhook payload for V1 manual testing
    from_number: str
    body: str

@router.post("/opt-in")
def opt_in_user(data: OptInRequest):
    """
    Registers the user and subscribes them to Salah accountability.
    """
    try:
        user_id = users.register_user(
            phone_number=data.phone_number,
            name=data.name,
            timezone=data.timezone,
            lat=data.latitude,
            lng=data.longitude
        )
        users.subscribe_habit(user_id, "salah", preferences=data.preferences)
        return {"status": "success", "user_id": user_id, "message": "Welcome to Rafeeq V1. Accountability active."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook/message")
def receive_message(payload: MessagePayload):
    """
    Endpoint to simulate receiving a WhatsApp message.
    Real WhatsApp Webhook would verify signature and parse complex JSON.
    This is for V1 manual testing via curl/Postman.
    """
    try:
        dispatcher.handle_incoming_message(payload.from_number, payload.body)
        return {"status": "received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
