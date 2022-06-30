import gzip
from flask import make_response, json
import pandas as pd
import numpy as np
import json
import khayyam


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


def read_json(dict_data):
    j_data = json.dumps(dict_data)
    data = pd.read_json(j_data)
    return data

def convert_to_miladi(date: str):
    parts = date.split('-')
    if len(parts) == 3:
        return khayyam.JalaliDate(parts[0], parts[1], parts[2]).todate()
    else:
        return khayyam.JalaliDatetime(int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]),
                                      int(parts[4]), int(parts[5]), int(parts[6])).todatetime()

def convert_to_shamsi(date, time_type):
    res = str(khayyam.JalaliDate(date))
    if time_type == 'daily':
        res = str(khayyam.JalaliDate(date))
        return res
    elif time_type == 'monthly':
        res = str(khayyam.JalaliDate(date)) 
        res = res.split('-')
        return res[0] + "-" + res[1]
    else:
        res = str(khayyam.JalaliDatetime(date))
        return res
