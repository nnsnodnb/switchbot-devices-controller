import os
from datetime import datetime
from pathlib import Path

from api.bitmeister import get_sun_moon_rise_set
from api.switchbot import SwitchBot
from aws.s3 import AlreadyExistObjectError, upload_source_code, upload_template
from curtain.timezone import ASIA_TOKYO
from misc.zipper import zip_folder

S3_BUCKET_NAME = os.environ["S3_BUCKET_NAME"]


def main() -> None:
    # default location is Tokyo station
    latitude = float(os.getenv("LATITUDE", "35.68137636985265"))
    longitude = float(os.getenv("LONGITUDE", "139.76703435645047"))

    now = datetime.now(tz=ASIA_TOKYO)
    sun_moon_rise_set = get_sun_moon_rise_set(date=now, latitude=latitude, longitude=longitude)

    base_dir = Path(__file__).parent

    # Upload source to S3 bucket
    archive_path = zip_folder(src=base_dir, dest=base_dir / "dist").absolute()
    try:
        source_code_s3_key = upload_source_code(source_code_path=archive_path, bucket_name=S3_BUCKET_NAME)
    except AlreadyExistObjectError as e:
        print(e)
        source_code_s3_key = e.s3_key
    print(f"{source_code_s3_key=}")
    # Upload template to S3 bucket
    template_path = Path(__file__).parent / "cloudformation" / "close_curtain.yml"
    try:
        template_s3_key = upload_template(template_path=template_path, bucket_name=S3_BUCKET_NAME)
    except AlreadyExistObjectError as e:
        print(e)
        template_s3_key = e.s3_key
    print(f"{template_s3_key=}")
    # 5. Exist check stack of CloudFormation
    # 6. Create CloudFormationStack if not exist and update if exist


def lambda_handler(event, context) -> None:
    token = os.environ["SWITCHBOT_API_TOKEN"]
    client_secret = os.environ["SWITCHBOT_API_CLIENT_SECRET"]

    switch_bot = SwitchBot(token=token, client_secret=client_secret)
    devices = filter(lambda device: device.is_curtain, switch_bot.get_devices())
    print(list(devices))


if __name__ == "__main__":
    main()
    # lambda_handler(None, None)
