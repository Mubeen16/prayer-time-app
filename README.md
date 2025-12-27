# Rafeeq (رفيق) - AI Accountability Partner

A transparent, educational, and accurate prayer time calculation engine.
Unlike generic apps, this project focuses on **fiqh transparency**, explaining *why* times are calculated the way they are, especially for high-latitude fallback and Asr differences.

## Features

- **Transparent Calculations**: Uses custom NOAA-style solar algorithms (`core/solar_calculations.py`). NO black-box libraries.
- **Fiqh Awareness**:
    - **Dual Asr**: Returns both Standard (Shafi/Maliki/Hanbali) and Hanafi Asr times.
    - **High Latitude**: Explicitly flags when "Middle of the Night" fallback is used for Fajr/Isha (e.g., in Oslo during summer).
- **Ad-Free API**: Simple REST API built with FastAPI.

## Usage

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the API
```bash
python api/main.py
```
Wrapper around `uvicorn`, runs on `http://0.0.0.0:8000`.

### 3. Endpoints

#### `GET /times`
Calculate prayer times.

**Parameters:**
- `lat`: Latitude (float)
- `lng`: Longitude (float)
- `date`: YYYY-MM-DD
- `timezone`: IANA timezone string (e.g., `Europe/Oslo`)
- `method`: Calculation method (Default: `MWL`)

**Example Request:**
```bash
curl "http://localhost:8000/times?lat=59.91&lng=10.75&date=2025-06-21&timezone=Europe/Oslo"
```

**Example Response:**
```json
{
  "date": "2025-06-21",
  "timezone": "Europe/Oslo",
  "method": "Muslim World League",
  "high_latitude_fallback": {
    "fajr": true,
    "isha": true,
    "method": "middle_of_the_night"
  },
  "times": {
    "fajr": "01:23",
    "sunrise": "03:53",
    "zuhr": "13:14",
    "asr": "17:42",
    "asr_standard": "17:42",
    "asr_hanafi": "19:05",
    "maghrib": "22:40",
    "isha": "00:58"
  }
}
```

#### `GET /methods`
List available calculation methods.

## Project Structure
- `api/`: FastAPI web layer
- `core/`: Pure Python logic (Solar physics + Prayer rules)
- `core/methods.py`: Juristic parameters (e.g., ISNA, MWL angles)
