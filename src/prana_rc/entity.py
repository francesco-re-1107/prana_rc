#    Prana RC
#    Copyright (C) 2020 Dmitry Berezovsky
#    
#    prana is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    
#    prana is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime
from enum import Enum
from typing import NamedTuple, List


class Speed(Enum):
    OFF = 0
    LOW = 1
    HIGH = 10
    SPEED_2 = 2
    SPEED_3 = 3
    SPEED_4 = 4
    SPEED_5 = 5
    SPEED_6 = 6
    SPEED_7 = 7
    SPEED_8 = 8
    SPEED_9 = 9

    @classmethod
    def all_options(self) -> List[str]:
        return ['low', 'l', 'high', 'h', 'off', 'stop', 2, 3, 4, 5, 6, 7, 8, 9]

    @classmethod
    def from_str(cls, speed: str) -> "Speed":
        speed = str(speed).lower().strip()
        if speed in ['low', 'l']:
            return cls.LOW
        if speed in ['high', 'h']:
            return cls.HIGH
        if speed in ['off', 'stop']:
            return cls.OFF
        try:
            speed_int = int(speed)
            if 0 <= speed_int <= 10:
                return cls(speed_int)
        except ValueError:
            pass
        raise ValueError('String {} is not valid speed identifier'.format(speed))

    def to_int(self) -> int:
        return int(self.value)


class Mode(Enum):
    NORMAL = 'normal'
    NIGHT = 'night'
    HIGH = 'high'


class PranaDeviceInfo(NamedTuple):
    address: str
    bt_device_name: str
    name: str
    rssi: int


class PranaState(object):

    def __init__(self) -> None:
        self.speed_locked: int = None
        self.speed_in: int = None
        self.speed_out: int = None
        self.night_mode: bool = None
        self.auto_mode: bool = None
        self.flows_locked: bool = None
        self.is_on: bool = None
        self.mini_heating_enabled: bool = None
        self.winter_mode_enabled: bool = None
        self.is_input_fan_on: bool = None
        self.is_output_fan_on: bool = None
        self.timestamp: datetime.datetime = None

    @property
    def speed(self):
        if not self.is_on:
            return 0
        return self.speed_locked if self.flows_locked else int((self.speed_in + self.speed_out) / 2)

    def __repr__(self):
        return "Prana state: {}, Speed: {}, Winter Mode: {}, Heating: {}, Flows locked: {}".format(
            'RUNNING' if self.is_on else 'IDLE',
            self.speed, self.winter_mode_enabled, self.mini_heating_enabled, self.flows_locked
        )
