import gzip
from flask import make_response, json
import pandas as pd
import numpy as np
import json
from khayyam import *
from utils.interpolation_methods import *
import dask
import dask.dataframe as dd

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

def convert_datetime_to_JalaliDatetime(df, config):
    shamsi_dates = list()
    for item in df["time"]:
        shamsi_dates.append(str(JalaliDatetime(item)))
    if(config['tool'] == 'Pandas'):
        shamsi_Series = pd.Series(shamsi_dates)
    elif(config['tool'] == 'Dask'):
        shamsi_Series_tmp = pd.Series(shamsi_dates)
        shamsi_Series = dd.from_pandas(shamsi_Series_tmp, npartitions=2)
    result = df.assign(time=shamsi_Series)
    return result

def convert_datetime_to_JalaliDatetime_for_skip_holiday_version(df, config):
    shamsi_dates = list()
    for item in df["time"]:
        shamsi_dates.append(JalaliDatetime(item))
    if (config['tool'] == 'Pandas'):
        shamsi_Series = pd.Series(shamsi_dates)
    elif (config['tool'] == 'Dask'):
        shamsi_Series_tmp = pd.Series(shamsi_dates)
        shamsi_Series = dd.from_pandas(shamsi_Series_tmp, npartitions=2)
    result = df.assign(time=shamsi_Series)
    return result


def convert_JalaliDatetime_to_datetime_for_skip_holiday_version(df, config):
    miladi_dates = list()
    for item in df["time"]:
        miladi_dates.append(item.todatetime())
    if (config['tool'] == 'Pandas'):
        miladi_Series = pd.Series(miladi_dates)
    elif (config['tool'] == 'Dask'):
        miladi_Series_tmp = pd.Series(miladi_dates)
        miladi_Series = dd.from_pandas(miladi_Series_tmp, npartitions=2)
    result = df.assign(time=miladi_Series)
    return result


def skip_holidays(data, config):
    data = convert_datetime_to_JalaliDatetime_for_skip_holiday_version(data, config)
    if(config['skip_holiday'] == True):
        for item in data['time']:
            if(item.weekday() == 6 or item.weekday() == 5):
                data.drop(data[data['time'] == item].index, inplace = True)
        data.reset_index(inplace = True)
        del data['index']
        data = convert_JalaliDatetime_to_datetime_for_skip_holiday_version(data, config)
        return data
    elif(config['skip_holiday'] == False):
        data = convert_JalaliDatetime_to_datetime_for_skip_holiday_version(data, config)
        return data

def interpolate(data,config):
    if(config['interpolation'] == 'linear'):
        return linear_interpolation(data, config)
    elif(config['interpolation'] == 'polynomial'):
        return polynomial_interpolation(data, config)
    elif(config['interpolation'] == 'spline'):
        return spline_interpolation(data, config)

def read_json_time_series(dict_data, config):#"1399-12-12 15:16:17.101" it is structure of our shamsi dates
    j_data = json.dumps(dict_data)
    data = pd.read_json(j_data)
    data.time = pd.to_datetime(data.time, unit='ms')
    if config['tool'] == 'Dask':
        data = dd.from_pandas(data, npartitions=10)
    return data