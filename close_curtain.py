import os
from datetime import datetime
from pathlib import Path

from api import SwitchBot, get_sun_rise_set
from aws.cloudformation import deploy_stack
from aws.s3 import AlreadyExistObjectError, upload_source_code, upload_template
from misc.schedule_expression import datetime_to_events_rule_schedule_expression
from misc.timezone import ASIA_TOKYO
from misc.zipper import zip_folder
from models import CloudFormationParameter, SunRiseSet

BASE_DIR = Path(__file__).parent
# Required environment variables
CFN_STACK_NAME = ""
S3_BUCKET_NAME = ""
SWITCHBOT_API_TOKEN = os.environ["SWITCHBOT_API_TOKEN"]
SWITCHBOT_API_CLIENT_SECRET = os.environ["SWITCHBOT_API_CLIENT_SECRET"]
# Optional environment variables
IS_CREATE_LOG_GROUP = os.environ.get("IS_CREATE_LOG_GROUP", "true")
USE_LOCALSTACK = os.environ.get("USE_LOCALSTACK", "false").lower() == "true"


def _get_sun_moon_rise_set() -> SunRiseSet:
    # default location is Tokyo station
    latitude = float(os.getenv("LATITUDE", "35.68137636985265"))
    longitude = float(os.getenv("LONGITUDE", "139.76703435645047"))

    now = datetime.now(tz=ASIA_TOKYO)
    sun_moon_rise_set = get_sun_rise_set(date=now, latitude=latitude, longitude=longitude)

    return sun_moon_rise_set


def _zipped_folder_and_upload_to_s3() -> (str, bool):
    archive_path = zip_folder(src=BASE_DIR, dest=BASE_DIR / "dist").absolute()
    try:
        s3_key = upload_source_code(source_code_path=archive_path, bucket_name=S3_BUCKET_NAME)
        print("Source code archive uploaded to S3 bucket.")
        return s3_key, True
    except AlreadyExistObjectError as e:
        print(e)
        return e.s3_key, False


def _upload_template_to_s3() -> (str, bool):
    template_path = Path(__file__).parent / "cloudformation" / "close_curtain.yml"
    try:
        s3_key = upload_template(template_path=template_path, bucket_name=S3_BUCKET_NAME)
        print("CloudFormation template uploaded to S3 bucket.")
        return s3_key, True
    except AlreadyExistObjectError as e:
        print(e)
        return e.s3_key, False


def _create_close_curtain_stack(source_code_s3_key: str, template_s3_key: str) -> str:
    sun_moon_rise_set = _get_sun_moon_rise_set()
    schedule_expression = datetime_to_events_rule_schedule_expression(
        date=sun_moon_rise_set.rise_and_set.sunset_datetime
    )

    cfn_params = [
        CloudFormationParameter(
            key="IsCreateLogGroup",
            value=IS_CREATE_LOG_GROUP,
        ),
        CloudFormationParameter(
            key="SwitchBotApiToken",
            value=SWITCHBOT_API_TOKEN,
        ),
        CloudFormationParameter(
            key="SwitchBotApiClientSecret",
            value=SWITCHBOT_API_CLIENT_SECRET,
        ),
        CloudFormationParameter(
            key="CloseCurtainFunctionS3BucketName",
            value=S3_BUCKET_NAME,
        ),
        CloudFormationParameter(
            key="CloseCurtainFunctionZipFileS3Key",
            value=source_code_s3_key,
        ),
        CloudFormationParameter(
            key="CloseCurtainEventScheduleExpression",
            value=schedule_expression,
        ),
    ]

    stack_id = deploy_stack(
        stack_name=CFN_STACK_NAME,
        template_s3_key=template_s3_key,
        parameters=cfn_params,
        bucket_name=S3_BUCKET_NAME,
        wait_complete=True,
        use_localstack=USE_LOCALSTACK,
    )

    return stack_id


def main() -> None:
    global CFN_STACK_NAME, S3_BUCKET_NAME
    CFN_STACK_NAME = os.environ.get("CFN_STACK_NAME", "CloseCurtainStack")
    S3_BUCKET_NAME = os.environ["S3_BUCKET_NAME"]

    # Upload source to S3 bucket
    source_code_s3_key, code_uploaded = _zipped_folder_and_upload_to_s3()
    # Upload template to S3 bucket
    template_s3_key, template_uploaded = _upload_template_to_s3()
    # Deploy CloudFormation Stack
    if not code_uploaded and not template_uploaded:
        print("No need to deploy.")
        return

    stack_id = _create_close_curtain_stack(
        source_code_s3_key=source_code_s3_key,
        template_s3_key=template_s3_key,
    )

    print(f"Deployed Stack ID: {stack_id}")


def lambda_handler(event, context) -> None:
    switch_bot = SwitchBot(
        token=SWITCHBOT_API_TOKEN,
        client_secret=SWITCHBOT_API_CLIENT_SECRET,
    )
    devices = filter(lambda d: d.is_curtain, switch_bot.get_devices())

    for device in devices:
        switch_bot.close_curtain(device=device)
        print(f"Closed {device.device_name}.")


if __name__ == "__main__":
    main()
