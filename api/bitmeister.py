import json
from datetime import datetime

import urllib3

from models import SunMoonRiseSet

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

    http = urllib3.PoolManager()
    res = http.request(
        method="GET",
        url=url,
        fields=params,
        headers=headers,
    )

    if res.status != 200:
        raise Exception(f'Failed to request to "GET {url}": {res.status}')

    data = json.loads(res.data.decode())
    print(url)
    print(data)

    return SunMoonRiseSet.from_dict(data=data, now=date)
