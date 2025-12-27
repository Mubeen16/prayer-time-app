from datetime import date
from core.prayer_times import get_prayer_times

result = get_prayer_times(
    latitude=59.9139,
    longitude=10.7522,
    on_date=date(2025, 6, 21),
    method_key="MWL",
    timezone="Europe/Oslo",
)

print(result)
