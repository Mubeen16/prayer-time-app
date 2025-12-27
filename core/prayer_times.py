# core/prayer_times.py
"""
Prayer time resolver.

Responsibilities:
- Load fiqh-based calculation methods
- Use solar_calculations for astronomy
- Apply Islamic prayer rules
- Handle high-latitude edge cases safely
"""

from datetime import date as Date
from zoneinfo import ZoneInfo

from core.methods import METHODS
from core import solar_calculations as solar


def middle_of_night(maghrib, sunrise):
    """
    High-latitude fallback.
    Returns the middle point between Maghrib and Sunrise.
    """
    night_duration = sunrise - maghrib
    return maghrib + (night_duration / 2)


def get_prayer_times(
    *,
    latitude: float,
    longitude: float,
    on_date: Date,
    method_key: str = "MWL",
    timezone: str = "Europe/London",
) -> dict:
    """
    Compute prayer times for a given location and date.

    Inputs:
      - latitude, longitude: GPS coordinates
      - on_date: datetime.date
      - method_key: key from METHODS (MWL, ISNA, UMM_AL_QURA, KARACHI)
      - timezone: IANA timezone string

    Returns:
      dict containing calculated prayer times
    """

    if method_key not in METHODS:
        raise ValueError(f"Unknown method '{method_key}'")

    method = METHODS[method_key]
    tz = ZoneInfo(timezone)

    # -----------------------
    # Solar anchor points
    # -----------------------
    sunrise = solar.sunrise(latitude, longitude, on_date, tz)
    sunset = solar.sunset(latitude, longitude, on_date, tz)
    solar_noon = solar.solar_noon(latitude, longitude, on_date, tz)

    maghrib = sunset

    # -----------------------
    # Fajr (with fallback)
    # -----------------------
    try:
        fajr = solar.time_when_sun_reaches_angle(
            latitude=latitude,
            longitude=longitude,
            on_date=on_date,
            tz=tz,
            angle_degrees=-method["fajr_angle"],
            direction="before",
        )
        fajr_fallback = False
    except ValueError:
        fajr = sunrise - (sunrise - maghrib) / 2
        fajr_fallback = True

    # -----------------------
    # Asr
    # -----------------------
    asr = solar.asr_time(
        latitude=latitude,
        longitude=longitude,
        on_date=on_date,
        tz=tz,
        asr_factor=method.get("asr_factor", 1),
    )

    # -----------------------
    # Isha (with fallback)
    # -----------------------
    try:
        if "isha_minutes" in method:
            isha = maghrib + solar.minutes(method["isha_minutes"])
        else:
            isha = solar.time_when_sun_reaches_angle(
                latitude=latitude,
                longitude=longitude,
                on_date=on_date,
                tz=tz,
                angle_degrees=-method["isha_angle"],
                direction="after",
            )
        isha_fallback = False
    except ValueError:
        isha = maghrib + (sunrise - maghrib) / 2
        isha_fallback = True

    # -----------------------
    # Output formatting
    # -----------------------
    def fmt(dt):
        return dt.strftime("%H:%M")

    return {
        "date": on_date.isoformat(),
        "timezone": timezone,
        "method": method["name"],
        "location": {
            "latitude": latitude,
            "longitude": longitude,
        },
        "high_latitude_fallback": {
            "fajr": fajr_fallback,
            "isha": isha_fallback,
            "method": "middle_of_the_night" if (fajr_fallback or isha_fallback) else None,
        },
        "times": {
            "fajr": fmt(fajr),
            "sunrise": fmt(sunrise),
            "zuhr": fmt(solar_noon),
            "asr": fmt(asr),
            "maghrib": fmt(maghrib),
            "isha": fmt(isha),
        },
    }
