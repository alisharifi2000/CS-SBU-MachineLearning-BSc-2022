from datetime import datetime
import gzip
from flask import make_response, json
import pandas as pd
import numpy as np
import json
from khayyam import JalaliDate, JalaliDatetime
from datetime import datetime


def response_message(data=None, status=200):
    if status in range(200, 400):
        content = gzip.compress(json.dumps(data, ensure_ascii=False, indent=3, default=convert,
                                           sort_keys=False).encode('utf8'), 5)
    else:
        content = gzip.compress(
            json.dumps({'message': data, 'status': 'error'}, ensure_ascii=False, indent=3).encode('utf-8'), 5)
    response = make_response(content, status)
    response.headers['Content-length'] = len(content)
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


def convert(o):
    if isinstance(o, np.int64):
        return int(o)
    if isinstance(o, np.bool_):
        if o:
            return True
        else:
            return False
    if pd.isna(o):
        return None

def convertShamsiToMilady(shamsiDateTime):
    shamsiDateTime = shamsiDateTime.split(sep='-')
    shamsiDateTime = JalaliDatetime(int(shamsiDateTime[0]), int(shamsiDateTime[1]), int(shamsiDateTime[2]), int(shamsiDateTime[3])
        , int(shamsiDateTime[4]), int(shamsiDateTime[5]), int(shamsiDateTime[6]))
    return shamsiDateTime.todatetime()

def read_json_time_series(dict_data, isShamsi):
    j_data = json.dumps(dict_data)
    data = pd.read_json(j_data)
    if isShamsi:
        data['time'] = data['time'].map(lambda d: convertShamsiToMilady(d))
    data.time = pd.to_datetime(data.time, unit='ms')

    # print(data.info())
    # print(data)
    return data