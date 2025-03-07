from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Self

from misc.timezone import ASIA_TOKYO


@dataclass
class Date:
    year: int
    month: int
    day: int

    def __post_init__(self) -> None:
        self.year = int(self.year)
        self.month = int(self.month)
        self.day = int(self.day)


@dataclass
class Coordinate:
    lat: str = field(repr=False)
    lng: str = field(repr=False)
    latitude: float = field(init=False)
    longitude: float = field(init=False)

    def __post_init__(self) -> None:
        self.latitude = float(self.lat)
        self.longitude = float(self.lng)


@dataclass(frozen=True)
class Location:
    coordinate: Coordinate


@dataclass(frozen=True)
class RiseAndSet:
    sunrise: float
    sunrise_hm: str
    sunrise_datetime: datetime = field(repr=False)
    sunset: float
    sunset_hm: str
    sunset_datetime: datetime = field(repr=False)

    @classmethod
    def from_dict(cls, data: dict[str, Any], now: datetime) -> Self:
        format_ = "%H:%M"
        sunrise_time = datetime.strptime(data["sunrise_hm"], format_).time()
        sunset_time = datetime.strptime(data["sunset_hm"], format_).time()
        data["sunrise_datetime"] = datetime.combine(now.date(), sunrise_time, tzinfo=ASIA_TOKYO)
        data["sunset_datetime"] = datetime.combine(now.date(), sunset_time, tzinfo=ASIA_TOKYO)

        return cls(**data)


@dataclass(frozen=True)
class SunRiseSet:
    date: Date
    location: Location
    rise_and_set: RiseAndSet
    version: str

    @classmethod
    def from_dict(cls, data: dict[str, Any], now: datetime) -> Self:
        date = Date(**data["date"])
        location = Location(coordinate=Coordinate(**data["location"]["coordinate"]))
        rise_and_set = RiseAndSet.from_dict(data=data["rise_and_set"], now=now)
        version = data["version"]

        return cls(
            date=date,
            location=location,
            rise_and_set=rise_and_set,
            version=version,
        )


@dataclass(frozen=True)
class SwitchBotDevice:
    device_id: str
    device_name: str
    device_type: str
    enable_cloud_service: bool
    hub_device_id: str
    curtain_devices_ids: list[str] | None
    calibrate: bool | None
    group: bool | None
    master: bool | None
    open_direction: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            device_id=data["deviceId"],
            device_name=data["deviceName"],
            device_type=data["deviceType"],
            enable_cloud_service=data["enableCloudService"],
            hub_device_id=data["hubDeviceId"],
            curtain_devices_ids=data.get("curtainDevicesIds"),
            calibrate=data.get("calibrate"),
            group=data.get("group"),
            master=data.get("master"),
            open_direction=data.get("openDirection"),
        )

    @property
    def is_curtain(self):
        return self.device_type in ("Curtain", "Curtain3")


@dataclass(frozen=True)
class CloudFormationParameter:
    key: str
    value: str | None
    use_previous_value: bool | None = field(default=None)

    def to_dict(self) -> dict[str, str]:
        result = {"ParameterKey": self.key}
        if self.value is not None:
            result["ParameterValue"] = self.value
        if self.use_previous_value is not None:
            result["UsePreviousValue"] = self.use_previous_value

        return result
