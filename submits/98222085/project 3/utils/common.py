import gzip
from flask import make_response, json
import pandas as pd
import numpy as np
import json
from khayyam import *
import re

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


def read_json_time_series(dict_data, type="miladi"):
    j_data = json.dumps(dict_data)
    data = pd.read_json(j_data)
    if type == "miladi":
        data.time = pd.to_datetime(data.time)
    elif type == "shamsi":
        miladi_equivalent_date = []
        vol = data['vol']
        for index in range(0, len(data)):
            y_str, m_str, d_str = re.split(r'\s|-', data.iloc[index]['time'])
            miladi_equivalent_date.append(JalaliDate(int(y_str), int(m_str), int(d_str)).todate())
        data.drop(['time', 'vol'], axis=1, inplace=True)
        data['time'] = miladi_equivalent_date
        data.time = pd.to_datetime(data.time)
        data['vol'] = vol

    return data


def read_json(dict_data):
    j_data = json.dumps(dict_data)
    data = pd.read_json(j_data)
    return data
