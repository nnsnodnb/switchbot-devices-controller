from datetime import datetime

import pytest

from misc.schedule_expression import datetime_to_events_rule_schedule_expression
from misc.timezone import ASIA_TOKYO


class TestDatetimeToEventsRuleScheduleExpression:
    @pytest.mark.parametrize(
        "offset_minutes, expected",
        [
            (None, "cron(30 8 22 2 ? 2025)"),
            (10, "cron(40 8 22 2 ? 2025)"),
        ],
    )
    def test_it(self, freezer, offset_minutes, expected):
        freezer.move_to("2025-02-22 17:30:00+09:00")
        now = datetime.now(tz=ASIA_TOKYO)

        actual = datetime_to_events_rule_schedule_expression(date=now, offset_minutes=offset_minutes)

        assert actual == expected
