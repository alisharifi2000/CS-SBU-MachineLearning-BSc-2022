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

def combine_results(result1,result2,config):
    id=list()
    time=list()
    method1=list()
    method2=list()
    if (config['time_series'] == True):
        for item in result1["time"]:
            time.append(item)
            final_result = pd.DataFrame(
                {
                    'time':pd.Series(time)
                }
            )
    elif (config['time_series'] == False):
        for item in result1["id"]:
            id.append(item)
            final_result = pd.DataFrame(
                {
                    'id': pd.Series(id)
                }
            )
    for item in result1["method1"]:
        method1.append(item)
        final_result["method1"] = pd.Series(method1)
    for item in result2["method2"]:
        method2.append(item)
        final_result["method2"] = pd.Series(method2)
    return final_result

def read_json(dict_data, config):
    j_data = json.dumps(dict_data)
    data = pd.read_json(j_data)
    return data