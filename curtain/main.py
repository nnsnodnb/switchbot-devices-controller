import os
from datetime import datetime

from curtain.api.bitmeister import get_sun_moon_rise_set
from curtain.timezone import ASIA_TOKYO

# default location is Tokyo station
LATITUDE = float(os.getenv("LATITUDE", "35.68137636985265"))
LONGITUDE = float(os.getenv("LONGITUDE", "139.76703435645047"))


if __name__ == "__main__":
    sun_moon_rise_set = get_sun_moon_rise_set(datetime.now(tz=ASIA_TOKYO), LATITUDE, LONGITUDE)
    print(sun_moon_rise_set)
