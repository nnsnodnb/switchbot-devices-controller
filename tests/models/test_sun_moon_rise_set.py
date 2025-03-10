from datetime import datetime
from typing import Any

from misc.timezone import ASIA_TOKYO
from models import SunRiseSet


def test_from_dict(sun_rise_set_json: dict[str, Any]):
    actual = SunRiseSet.from_dict(data=sun_rise_set_json, now=datetime.now(tz=ASIA_TOKYO))

    assert actual.date.year == 2025
    assert actual.date.month == 2
    assert actual.date.day == 15
    assert actual.location.coordinate.latitude == 35.68137636985265
    assert actual.location.coordinate.longitude == 139.76703435645047
    assert actual.rise_and_set.sunrise == 6.465
    assert actual.rise_and_set.sunrise_hm == "6:27"
    assert actual.rise_and_set.sunset == 17.376
    assert actual.rise_and_set.sunset_hm == "17:23"
    assert actual.version == "2.2"
