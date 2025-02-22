from datetime import datetime

import requests

from ..models import SunMoonRiseSet

BASE_URL = "https://labs.bitmeister.jp"


def get_sun_moon_rise_set(date: datetime, latitude: float, longitude: float) -> SunMoonRiseSet:
    url = f"{BASE_URL}/ohakon/json"
    params = {
        "mode": "sun_moon_rise_set",
        "year": date.year,
        "month": date.month,
        "day": date.day,
        "lat": latitude,
        "lng": longitude,
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    res = requests.get(url=url, params=params, headers=headers)
    res.raise_for_status()

    data = res.json()

    return SunMoonRiseSet.from_dict(data)
