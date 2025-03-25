from datetime import datetime, timedelta

from misc.timezone import UTC


def datetime_to_events_rule_schedule_expression(date: datetime, offset_minutes: int | None = None) -> str:
    # There may be cases where an offset is set because there is time from sunset until it gets dark.
    if offset_minutes is not None:
        date += timedelta(minutes=offset_minutes)

    utc_date = date.astimezone(tz=UTC)
    return f"cron({utc_date.minute} {utc_date.hour} {utc_date.day} {utc_date.month} ? {utc_date.year})"
