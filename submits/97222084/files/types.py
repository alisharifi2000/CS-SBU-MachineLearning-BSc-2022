from enum import Enum
from typing import Optional
from pydantic import BaseModel


class Calender_Type(str, Enum):
    shamsi = 'shamsi'
    miladi = 'miladi'


class Calender_Time(str, Enum):
    daily = 'daily'
    monthly = 'monthly'


class Method(str, Enum):
    linear = 'linear'


class SamplingMethods(BaseModel):
    undersampling = 'undersampling'
    oversampling = 'oversampling'
    SMOTE = 'SMOTE'


class Config(BaseModel):
    type: Calender_Type
    time: Calender_Time
    interpolation: Method


class ConfigOfTimeSwitch(BaseModel):
    time: Calender_Time
    interpolation: Method
    skip_holiday: Optional[bool]


class ConfigOfDetection(BaseModel):
    timeseries: bool


class BalancedConfig(BaseModel):
    major_class_tag: str
    minor_class_tag: str
    method: SamplingMethods