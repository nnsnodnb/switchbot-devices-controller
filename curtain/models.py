from dataclasses import dataclass, field
from typing import Any, Self


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
    moonrise: float
    moonrise_hm: str
    moonset: float
    moonset_hm: str
    sunrise: float
    sunrise_hm: str
    sunset: float
    sunset_hm: str


@dataclass(frozen=True)
class SunMoonRiseSet:
    date: Date
    location: Location
    moon_age: float
    rise_and_set: RiseAndSet
    version: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        date = Date(**data["date"])
        location = Location(coordinate=Coordinate(**data["location"]["coordinate"]))
        moon_age = float(data["moon_age"])
        rise_and_set = RiseAndSet(**data["rise_and_set"])
        version = data["version"]

        return cls(
            date=date,
            location=location,
            moon_age=moon_age,
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
