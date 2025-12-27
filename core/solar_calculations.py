# core/solar_calculations.py
# Accuracy-first, transparent solar math (NOAA-style approximations).
# This module is PURE astronomy: sunrise/sunset/solar-noon and “sun at altitude angle”.

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date as Date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from typing import Literal


# -----------------------------
# Small helpers
# -----------------------------

def minutes(n: int) -> timedelta:
    return timedelta(minutes=n)


def _deg2rad(d: float) -> float:
    return d * math.pi / 180.0


def _rad2deg(r: float) -> float:
    return r * 180.0 / math.pi


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


# -----------------------------
# Core solar model (NOAA-style)
# -----------------------------

@dataclass(frozen=True)
class _SolarState:
    """Solar quantities for a given moment (in UTC)."""
    declination_rad: float
    eq_time_minutes: float  # equation of time in minutes


def _julian_day(dt_utc: datetime) -> float:
    """
    Julian Day for a UTC datetime.
    Valid for modern dates. Uses standard astronomical conversion.
    """
    if dt_utc.tzinfo is None:
        raise ValueError("dt_utc must be timezone-aware (UTC).")
    dt_utc = dt_utc.astimezone(timezone.utc)

    year = dt_utc.year
    month = dt_utc.month
    day = dt_utc.day
    hour = dt_utc.hour + dt_utc.minute / 60 + dt_utc.second / 3600 + dt_utc.microsecond / 3.6e9

    if month <= 2:
        year -= 1
        month += 12

    A = year // 100
    B = 2 - A + (A // 4)

    jd_day = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5
    jd = jd_day + hour / 24.0
    return jd


def _julian_century(jd: float) -> float:
    return (jd - 2451545.0) / 36525.0


def _solar_state(dt_utc: datetime) -> _SolarState:
    """
    Compute solar declination and equation of time using NOAA Solar Calculator style formulas.
    """
    jd = _julian_day(dt_utc)
    T = _julian_century(jd)

    # Geometric mean longitude of the sun (deg)
    L0 = (280.46646 + T * (36000.76983 + 0.0003032 * T)) % 360.0

    # Geometric mean anomaly (deg)
    M = 357.52911 + T * (35999.05029 - 0.0001537 * T)

    # Eccentricity of Earth's orbit
    e = 0.016708634 - T * (0.000042037 + 0.0000001267 * T)

    # Sun equation of center (deg)
    Mrad = _deg2rad(M)
    C = (
        math.sin(Mrad) * (1.914602 - T * (0.004817 + 0.000014 * T))
        + math.sin(2 * Mrad) * (0.019993 - 0.000101 * T)
        + math.sin(3 * Mrad) * 0.000289
    )

    # True longitude (deg)
    true_long = L0 + C

    # Apparent longitude (deg)
    omega = 125.04 - 1934.136 * T
    lambda_sun = true_long - 0.00569 - 0.00478 * math.sin(_deg2rad(omega))

    # Mean obliquity of the ecliptic (deg)
    eps0 = 23.0 + (26.0 + ((21.448 - T * (46.815 + T * (0.00059 - T * 0.001813))) / 60.0)) / 60.0
    # Corrected obliquity (deg)
    eps = eps0 + 0.00256 * math.cos(_deg2rad(omega))

    # Declination (rad)
    decl = math.asin(math.sin(_deg2rad(eps)) * math.sin(_deg2rad(lambda_sun)))

    # Equation of time (minutes)
    y = math.tan(_deg2rad(eps) / 2.0)
    y *= y

    L0rad = _deg2rad(L0)
    lambdar = _deg2rad(lambda_sun)

    eq_time = 4.0 * _rad2deg(
        y * math.sin(2.0 * L0rad)
        - 2.0 * e * math.sin(Mrad)
        + 4.0 * e * y * math.sin(Mrad) * math.cos(2.0 * L0rad)
        - 0.5 * y * y * math.sin(4.0 * L0rad)
        - 1.25 * e * e * math.sin(2.0 * Mrad)
    )

    return _SolarState(declination_rad=decl, eq_time_minutes=eq_time)


def _solar_noon_utc(latitude: float, longitude: float, on_date: Date) -> datetime:
    """
    Approximate solar noon in UTC for the given date.
    NOAA approach:
      solarNoonUTC (minutes) ~= 720 - 4*longitude - eqTime
    where longitude is degrees (east positive).
    """
    # Start with 12:00 UTC as a reference moment on that date
    base = datetime(on_date.year, on_date.month, on_date.day, 12, 0, tzinfo=timezone.utc)
    state = _solar_state(base)
    minutes_utc = 720.0 - 4.0 * longitude - state.eq_time_minutes
    return datetime(on_date.year, on_date.month, on_date.day, tzinfo=timezone.utc) + timedelta(minutes=minutes_utc)


def solar_noon(latitude: float, longitude: float, on_date: Date, tz: ZoneInfo) -> datetime:
    dt_utc = _solar_noon_utc(latitude, longitude, on_date)
    return dt_utc.astimezone(tz)


def _hour_angle_for_altitude(
    latitude_deg: float,
    declination_rad: float,
    altitude_deg: float,
) -> float:
    """
    Solve for hour angle H (radians) when solar altitude equals altitude_deg.

    sin(alt) = sin(lat)*sin(dec) + cos(lat)*cos(dec)*cos(H)
    => cos(H) = (sin(alt) - sin(lat)*sin(dec)) / (cos(lat)*cos(dec))
    """
    lat = _deg2rad(latitude_deg)
    alt = _deg2rad(altitude_deg)

    sin_alt = math.sin(alt)
    sin_lat = math.sin(lat)
    cos_lat = math.cos(lat)

    sin_dec = math.sin(declination_rad)
    cos_dec = math.cos(declination_rad)

    denom = cos_lat * cos_dec
    if abs(denom) < 1e-12:
        # Extremely close to poles; can still be handled but likely polar day/night edge cases.
        raise ValueError("Hour angle undefined at this latitude/declination (polar edge case).")

    cosH = (sin_alt - sin_lat * sin_dec) / denom
    cosH = _clamp(cosH, -1.0, 1.0)

    return math.acos(cosH)  # radians, always positive


def _event_time_utc(
    latitude: float,
    longitude: float,
    on_date: Date,
    altitude_deg: float,
    direction: Literal["before", "after"],
) -> datetime:
    """
    Compute UTC time when the sun reaches a given altitude on the given date.

    direction:
      - "before": morning event (before solar noon)
      - "after" : evening event (after solar noon)

    If the sun never reaches the altitude (polar day/night), raises ValueError.
    """
    # 1) Solar noon in UTC
    noon_utc = _solar_noon_utc(latitude, longitude, on_date)

    # 2) Solar state at noon (good approximation for the day)
    state = _solar_state(noon_utc)
    dec = state.declination_rad
    eq_time = state.eq_time_minutes

    # 3) Hour angle for desired altitude
    # If the sun never reaches that altitude, acos input will clamp,
    # but we detect reachability by checking unclamped value.
    lat = _deg2rad(latitude)
    alt = _deg2rad(altitude_deg)

    sin_alt = math.sin(alt)
    sin_lat = math.sin(lat)
    cos_lat = math.cos(lat)
    sin_dec = math.sin(dec)
    cos_dec = math.cos(dec)

    denom = cos_lat * cos_dec
    if abs(denom) < 1e-12:
        raise ValueError("Polar edge case: cannot compute for this location/date.")

    cosH_raw = (sin_alt - sin_lat * sin_dec) / denom
    if cosH_raw < -1.0 or cosH_raw > 1.0:
        # No solution: sun never reaches that altitude
        raise ValueError("No event time: sun does not reach this altitude on this date at this location.")

    H = math.acos(_clamp(cosH_raw, -1.0, 1.0))  # radians
    H_deg = _rad2deg(H)

    # 4) Convert hour angle to minutes from solar noon
    delta_minutes = 4.0 * H_deg  # 1 degree = 4 minutes

    # Noon in minutes from 00:00 UTC using NOAA formula:
    # solarNoonUTC = 720 - 4*longitude - eqTime
    solar_noon_minutes = 720.0 - 4.0 * longitude - eq_time

    if direction == "before":
        event_minutes = solar_noon_minutes - delta_minutes
    else:
        event_minutes = solar_noon_minutes + delta_minutes

    # normalize to within day (still safe if a few minutes outside due to approximations)
    dt0 = datetime(on_date.year, on_date.month, on_date.day, tzinfo=timezone.utc)
    return dt0 + timedelta(minutes=event_minutes)


# -----------------------------
# Public API functions
# -----------------------------

def sunrise(latitude: float, longitude: float, on_date: Date, tz: ZoneInfo) -> datetime:
    """
    Sunrise: standard altitude about -0.833 degrees (refraction + solar radius).
    """
    dt_utc = _event_time_utc(latitude, longitude, on_date, altitude_deg=-0.833, direction="before")
    return dt_utc.astimezone(tz)


def sunset(latitude: float, longitude: float, on_date: Date, tz: ZoneInfo) -> datetime:
    dt_utc = _event_time_utc(latitude, longitude, on_date, altitude_deg=-0.833, direction="after")
    return dt_utc.astimezone(tz)


def time_when_sun_reaches_angle(
    *,
    latitude: float,
    longitude: float,
    on_date: Date,
    tz: ZoneInfo,
    angle_degrees: float,
    direction: Literal["before", "after"],
) -> datetime:
    """
    General solver:
      angle_degrees is solar altitude in degrees.
      For “below horizon”, pass negative values (e.g., -18 for Fajr).
    """
    dt_utc = _event_time_utc(latitude, longitude, on_date, altitude_deg=angle_degrees, direction=direction)
    return dt_utc.astimezone(tz)


def asr_time(
    *,
    latitude: float,
    longitude: float,
    on_date: Date,
    tz: ZoneInfo,
    asr_factor: int = 1,
) -> datetime:
    """
    Asr is based on shadow length:
      asr_factor = 1 (Shafi'i/Maliki/Hanbali)
      asr_factor = 2 (Hanafi)

    We compute the required solar altitude for Asr and then solve for the time after noon.
    A common formulation:
      tan(alt) = 1 / (n + tan(|lat - decl|))
    where n is asr_factor and decl is solar declination.

    This yields an altitude (positive), then we find the afternoon time the sun reaches it.
    """
    if asr_factor not in (1, 2):
        raise ValueError("asr_factor must be 1 or 2.")

    noon_utc = _solar_noon_utc(latitude, longitude, on_date)
    state = _solar_state(noon_utc)
    decl = state.declination_rad

    lat_rad = _deg2rad(latitude)
    # |lat - decl| in radians
    phi = abs(lat_rad - decl)

    # altitude for Asr (radians)
    # tan(alt) = 1 / (n + tan(phi))
    alt_rad = math.atan(1.0 / (asr_factor + math.tan(phi)))
    alt_deg = _rad2deg(alt_rad)

    # Asr is always after solar noon
    dt_utc = _event_time_utc(latitude, longitude, on_date, altitude_deg=alt_deg, direction="after")
    return dt_utc.astimezone(tz)
