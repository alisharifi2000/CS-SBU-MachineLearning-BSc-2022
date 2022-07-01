import gzip
import json
import time

import numpy as np
import pandas as pd
from flask import json
from khayyam import JalaliDatetime


def read_json_time_series(dict_data, type):
    j_data = json.dumps(dict_data)
    data = pd.read_json(j_data)
    if type == "shamsi":
        for _ in range(len(data.time)):
            ls = data.time[_].split("-")
            data.time[_] = JalaliDatetime(ls[0], ls[1], ls[2]).todatetime()
    elif type == "miladi":
        data.time = pd.to_datetime(data.time, unit='ms')
    else:
        raise ValueError("Unknown type")
    return data

def read_time_series(dict_data):
    j_data = json.dumps(dict_data)
    data = pd.read_json(j_data)
    data.feature = pd.to_datetime(data.feature)
    for _ in range(len(data.feature)):
        data.feature[_] = int(time.mktime(data.feature[_].timetuple()))
    return data

def json_to_panda(dict_data):
    j_data = json.dumps(dict_data)
    data = pd.read_json(j_data)
    return data

def return_data(result):
    return dict({"data": result})

def miladi_to_shamsi(result):
    for _ in range(len(result["time"])):
        result["time"][_] = JalaliDatetime(result["time"][_]).isoformat()
    return result    
