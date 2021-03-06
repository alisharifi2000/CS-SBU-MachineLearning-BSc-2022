import gzip
from flask import make_response, json
import pandas as pd
import numpy as np
import json

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


def read_json_time_series(dict_data):
    j_data = json.dumps(dict_data)
    data = pd.read_json(j_data)
   # config['type'] == 'miladi':
    data.time = pd.to_datetime(data.time, unit='ms')
    return data
def read_json_simple(dict_data):
    j_data = json.dumps(dict_data)
    data = pd.read_json(j_data)
    return data

#def read_json_time_series(dict_data):
  #  j_data = json.dumps(dict_data)
  #  data = pd.read_json(j_data)
   # data.time = pd.to_datetime(data.time, unit='ms')
   # return data