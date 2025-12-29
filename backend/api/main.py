from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import date
from core.prayer_times import get_prayer_times
from fastapi.middleware.cors import CORSMiddleware

from core.methods import METHODS
from core.scheduler import calculate_schedule
from typing import List, Optional
from api import rafeeq

app = FastAPI(
    title="Al-Vaqth API",
    description="Backend for Al-Vaqth - The Prayer Time Engine.",
    version="1.0.0"
)

# CORS (Required for React Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In prod, specify the exact origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rafeeq.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

class PrayerTimesRequest(BaseModel):
    latitude: float
    longitude: float
    date: date
    method: str = "MWL"

    timezone: str = "UTC"

class TaskItem(BaseModel):
    name: str
    duration_minutes: int
    type: str = "shallow"  # 'deep' or 'shallow'

class ScheduleRequest(BaseModel):
    latitude: float
    longitude: float
    date: date
    timezone: str
    method: str = "MWL"
    tasks: List[TaskItem]

@app.get("/")
def read_root():
    return FileResponse('static/index.html')

@app.get("/methods")
def list_methods():
    """
    Returns a list of supported calculation methods.
    """
    return {key: val["name"] for key, val in METHODS.items()}

@app.get("/times")
def calculate_times(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    date_str: date = Query(..., alias="date", description="Date in YYYY-MM-DD format"),
    method: str = Query("MWL", description="Calculation method key (e.g. MWL, ISNA, KARACHI)"),
    timezone: str = Query("Europe/London", description="IANA Timezone string")
):
    """
    Calculate prayer times for a specific location and date.
    Returns standard and Hanafi Asr times, and high-latitude fallback info.
    """
    if method not in METHODS:
        supported = ", ".join(METHODS.keys())
        raise HTTPException(status_code=400, detail=f"Unknown method '{method}'. Supported: {supported}")

    try:
        result = get_prayer_times(
            latitude=lat,
            longitude=lng,
            on_date=date_str,
            method_key=method,
            timezone=timezone
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/schedule")
def generate_schedule(req: ScheduleRequest):
    """
    Generate a faith-optimized schedule based on prayer times.
    """
    try:
        # 1. Get Prayer Times
        prayer_data = get_prayer_times(
            latitude=req.latitude,
            longitude=req.longitude,
            on_date=req.date,
            method_key=req.method,
            timezone=req.timezone
        )
        
        # 2. Convert Pydantic models to dicts for the core logic
        task_list = [t.dict() for t in req.tasks]
        
        # 3. Calculate Schedule
        schedule = calculate_schedule(task_list, prayer_data)
        
        return {
            "date": req.date,
            "prayer_times": prayer_data['times'],
            "schedule": schedule
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
