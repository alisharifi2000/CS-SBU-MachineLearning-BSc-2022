from datetime import datetime, timedelta
from random import randint, seed
import pandas as pd
from typing import Dict
import time
import json

seed(time.time())


class TestDataSeries:
    def __init__(
            self,
            mode: str = 'miladi',
            start_time: datetime = datetime(year=2021, month=4, day=11),
            end_time: datetime = datetime(year=2022, month=4, day=11),
            timeframe: int = 60 * 60 * 24
        ) -> None:
        t = {
            60 * 60 * 24: timedelta(days=1),
            60 * 60 * 24 * 30: timedelta(weeks=4)
        }

        self.mode = mode
        self.timeframe = timeframe
        self.start_time = start_time
        self.end_time = end_time
        self.timeseries = {}
        self.time_delta = t[timeframe]

    def generate_dict(self):
        df = pd.DataFrame(columns=['time', 'vol'])
        df['time'] = [(i * self.time_delta + self.start_time).strftime(r'%Y/%m/%d')
                      for i in range(((self.end_time - self.start_time) / self.timeframe).seconds)]
        df['vol'] = [randint(1, 10**4) for i in range(((self.end_time - self.start_time) / self.timeframe).seconds)]

        return df.to_dict()

    def save_dict(self, _dict: Dict, filename: str = ''):
        if not filename:
            filename = f'{self.start_time}-{self.end_time}-{self.timeframe}-{self.mode}.csv'
        with open(filename, 'w') as f:
            json.dump(_dict, f)



timeseries = TestDataSeries(timeframe=60 * 60 * 24)
timeseries.save_dict(timeseries.generate_dict())