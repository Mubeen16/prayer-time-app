from datetime import date
from zoneinfo import ZoneInfo
from core.solar_calculations import sunrise, sunset, solar_noon, time_when_sun_reaches_angle, asr_time

lat, lon = 51.5074, -0.1278
tz = ZoneInfo("Europe/London")
d = date.today()

print("Sunrise:", sunrise(lat, lon, d, tz))
print("Solar noon:", solar_noon(lat, lon, d, tz))
print("Sunset:", sunset(lat, lon, d, tz))

print("Fajr-ish (alt -18):", time_when_sun_reaches_angle(
    latitude=lat, longitude=lon, on_date=d, tz=tz, angle_degrees=-18, direction="before"
))
print("Isha-ish (alt -17):", time_when_sun_reaches_angle(
    latitude=lat, longitude=lon, on_date=d, tz=tz, angle_degrees=-17, direction="after"
))
print("Asr (factor 1):", asr_time(latitude=lat, longitude=lon, on_date=d, tz=tz, asr_factor=1))
