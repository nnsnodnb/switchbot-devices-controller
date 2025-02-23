import json
from pathlib import Path
from typing import Any

import pytest


@pytest.fixture(scope="session")
def sun_moon_rise_set_json() -> dict[str, Any]:
    json_path = Path(__file__).parent / "fixtures" / "sun_moon_rise_set.json"
    json_data = json_path.read_text()

    return json.loads(json_data)
