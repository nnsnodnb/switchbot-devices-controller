from datetime import datetime

from misc.timezone import UTC


def datetime_to_events_rule_schedule_expression(date: datetime) -> str:
    utc_date = date.astimezone(tz=UTC)
    return f"cron({utc_date.minute} {utc_date.hour} {utc_date.day} {utc_date.month} ? {utc_date.year})"
