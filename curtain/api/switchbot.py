import base64
import hashlib
import hmac
import time
import uuid
from dataclasses import dataclass, field
from enum import StrEnum

import requests

from ..models import SwitchBotDevice


class SwitchBotApiEndpoint(StrEnum):
    DEVICES = "devices"


@dataclass(repr=False, frozen=True)
class SwitchBot:
    base_url: str = field(default="https://api.switch-bot.com", init=False, repr=False)
    version: str = field(default="v1.1", init=False)
    token: str = field(repr=False)
    client_secret: str = field(repr=False)

    def _make_endpoint_url(self, endpoint: SwitchBotApiEndpoint) -> str:
        return "/".join([self.base_url, self.version, endpoint.value])

    def _generate_signature(self, nonce: uuid.UUID, timestamp: int) -> str:
        msg = f"{self.token}{timestamp}{nonce}".encode()

        digest = hmac.new(key=self.client_secret.encode("utf-8"), msg=msg, digestmod=hashlib.sha256).digest()
        sign = base64.b64encode(digest).decode("utf-8")

        return sign

    def _get_headers(self) -> dict[str, str]:
        nonce = uuid.uuid4()
        timestamp = int(round(time.time() * 1000))
        signature = self._generate_signature(nonce=nonce, timestamp=timestamp)

        headers = {
            "Authorization": self.token,
            "Content-Type": "application/json",
            "charset": "utf8",
            "t": str(timestamp),
            "sign": signature,
            "nonce": str(nonce),
        }

        return headers

    def get_devices(self) -> list[SwitchBotDevice]:
        url = self._make_endpoint_url(SwitchBotApiEndpoint.DEVICES)
        headers = self._get_headers()

        res = requests.get(url=url, headers=headers)
        res.raise_for_status()

        data = res.json()

        return [SwitchBotDevice.from_dict(device) for device in data["body"]["deviceList"]]
