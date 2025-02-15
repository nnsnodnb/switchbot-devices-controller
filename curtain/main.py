import os

# from curtain.api.bitmeister import get_sun_moon_rise_set
from .api.switchbot import SwitchBot

# from curtain.api.switchbot import SwitchBot

# from curtain.timezone import ASIA_TOKYO

# default location is Tokyo station
LATITUDE = float(os.getenv("LATITUDE", "35.68137636985265"))
LONGITUDE = float(os.getenv("LONGITUDE", "139.76703435645047"))
SWITCHBOT_API_TOKEN = os.environ["SWITCHBOT_API_TOKEN"]
SWITCHBOT_API_CLIENT_SECRET = os.environ["SWITCHBOT_API_CLIENT_SECRET"]


if __name__ == "__main__":
    # sun_moon_rise_set = get_sun_moon_rise_set(datetime.now(tz=ASIA_TOKYO), LATITUDE, LONGITUDE)
    # print(sun_moon_rise_set)

    switch_bot = SwitchBot(
        token=SWITCHBOT_API_TOKEN,
        client_secret=SWITCHBOT_API_CLIENT_SECRET,
    )
    devices = switch_bot.get_devices()
    print(devices)
