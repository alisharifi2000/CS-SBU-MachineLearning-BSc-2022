from enum import Enum
from typing import Optional
from pydantic import BaseModel


class CalenderType(str, Enum):
    shamsi = 'shamsi'
    miladi = 'miladi'


class CalenderTime(str, Enum):
    daily = 'daily'
    monthly = 'monthly'


class InterMethod(str, Enum):
    linear = 'linear'


class SamplingMethods(BaseModel):
    undersampling = 'undersampling'
    oversampling = 'oversampling'
    SMOTE = 'SMOTE'


class Config(BaseModel):
    type: CalenderType
    time: CalenderTime
    interpolation: InterMethod


class ConfigTimeSwitch(BaseModel):
    time: CalenderTime
    interpolation: InterMethod
    skip_holiday: Optional[bool]


class ConfigDetection(BaseModel):
    timeseries: bool


class ConfigBalanced(BaseModel):
    major_class_tag: str
    minor_class_tag: str
    method: SamplingMethods