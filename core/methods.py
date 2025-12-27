# core/methods.py
"""
Prayer time calculation methods.

This module contains ONLY scholarly parameters.
No astronomy. No time calculations.

References:
- Muslim World League
- ISNA
- Umm al-Qura (Makkah)
- University of Karachi
"""

METHODS = {
    # Muslim World League
    "MWL": {
        "name": "Muslim World League",
        "fajr_angle": 18.0,
        "isha_angle": 17.0,
        "asr_factor": 1,
    },

    # Islamic Society of North America
    "ISNA": {
        "name": "Islamic Society of North America",
        "fajr_angle": 15.0,
        "isha_angle": 15.0,
        "asr_factor": 1,
    },

    # Umm al-Qura University (Makkah)
    # Isha is fixed minutes after Maghrib
    "UMM_AL_QURA": {
        "name": "Umm al-Qura University (Makkah)",
        "fajr_angle": 18.5,
        "isha_minutes": 90,     # 90 min after Maghrib (120 in Ramadan – NOT handled here)
        "asr_factor": 1,
    },

    # Karachi method (Hanafi Asr)
    "KARACHI": {
        "name": "University of Karachi",
        "fajr_angle": 18.0,
        "isha_angle": 18.0,
        "asr_factor": 2,        # Hanafi
    },
}
