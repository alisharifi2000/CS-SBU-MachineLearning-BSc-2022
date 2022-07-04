import pandas as pd
import numpy as np
from khayyam import JalaliDate, JalaliDatetime
from .types import Calender_Time

def linear_interpolation(data: pd.DataFrame, config):
    if config.time == Calender_Time.daily:
        data = data.set_index('time')
        data = data.resample('D')
        data = data.interpolate(method=config.interpolation)
        if 'skip_holiday' in config.dict():
            if config.skip_holiday:
                a = []
                for time_ in data.index :
                    if JalaliDatetime(time_.date()).isoweekday() != 7:
                        a.append(JalaliDatetime(time_.date()).strftime(r'%Y/%m/%d'))
                    else:
                        a.append(np.nan)
                data.index = a
            else:
                data.index = [JalaliDatetime(time_.date()).strftime(r'%Y/%m/%d') for time_ in data.index]
        data.reset_index(inplace=True)
        data.dropna(inplace=True)

    elif config.time == Calender_Time.monthly:
        data = data.set_index('time')
        data = data.resample('M')
        data = data.interpolate(method=config.interpolation)
        if 'skip_holiday' in config.dict():
            if config.skip_holiday:
                a = []
                for time_ in data.index :
                    if JalaliDatetime(time_.date()).isoweekday() != 7:
                        a.append(JalaliDatetime(time_.date()).strftime(r'%Y/%m/%d'))
                    else:
                        a.append(np.nan)
                data.index = a
                data.dropna(inplace=True)
            else:
                data.index = [JalaliDatetime(time_.date()).strftime(r'%Y/%m/%d') for time_ in data.index]
        data.reset_index(inplace=True)
        data.dropna(inplace=True)

    else:
        data = None

    return data