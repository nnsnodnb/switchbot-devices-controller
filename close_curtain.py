import os
from datetime import datetime

from api.bitmeister import get_sun_moon_rise_set
from api.switchbot import SwitchBot
from curtain.timezone import ASIA_TOKYO


def main() -> None:
    # default location is Tokyo station
    latitude = float(os.getenv("LATITUDE", "35.68137636985265"))
    longitude = float(os.getenv("LONGITUDE", "139.76703435645047"))

    now = datetime.now(tz=ASIA_TOKYO)
    sun_moon_rise_set = get_sun_moon_rise_set(date=now, latitude=latitude, longitude=longitude)
    print(sun_moon_rise_set)


def lambda_handler(event, context) -> None:
    token = os.environ["SWITCHBOT_API_TOKEN"]
    client_secret = os.environ["SWITCHBOT_API_CLIENT_SECRET"]

    switch_bot = SwitchBot(token=token, client_secret=client_secret)
    devices = filter(lambda device: device.is_curtain, switch_bot.get_devices())
    print(list(devices))


if __name__ == "__main__":
    main()
    lambda_handler(None, None)
