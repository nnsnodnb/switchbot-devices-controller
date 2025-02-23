from datetime import datetime

from curtain.schedule_expression import datetime_to_events_rule_schedule_expression
from curtain.timezone import ASIA_TOKYO


class TestDatetimeToEventsRuleScheduleExpression:
    def test_it(self, freezer):
        freezer.move_to("2025-02-22 17:30:00+09:00")
        now = datetime.now(tz=ASIA_TOKYO)

        actual = datetime_to_events_rule_schedule_expression(date=now)

        assert actual == "cron(30 8 22 2 ? 2025)"
