import json
import urllib.parse
import urllib.request
from datetime import datetime

from ..models import SunMoonRiseSet

BASE_URL = "https://labs.bitmeister.jp"


class SunMoonRiseSetAPIException(Exception):
    pass


def get_sun_moon_rise_set(date: datetime, latitude: float, longitude: float) -> SunMoonRiseSet:
    req_endpoint = f"{BASE_URL}/ohakon/json"

    query = {
        "mode": "sun_moon_rise_set",
        "year": date.year,
        "month": date.month,
        "day": date.day,
        "lat": latitude,
        "lng": longitude,
    }
    query_str = urllib.parse.urlencode(query)
    url = f"{req_endpoint}?{query_str}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    req = urllib.request.Request(url=url, headers=headers)

    with urllib.request.urlopen(req) as res:
        if res.status != 200:
            raise SunMoonRiseSetAPIException(f"Failed to get sun moon rise set. status={res.status}")

        data = json.loads(res.read())

    return SunMoonRiseSet.from_dict(data)
