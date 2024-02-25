from dataclasses import dataclass
from datetime import datetime
from .temperature import Temperature
from .gps import Gps


@dataclass
class AggregatedTemperature:
    temperature: Temperature
    gps: Gps
    time: datetime
