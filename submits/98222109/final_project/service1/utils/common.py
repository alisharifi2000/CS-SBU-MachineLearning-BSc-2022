import gzip
from flask import make_response, json
import pandas as pd
import numpy as np
import json
from datetime import *
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


def convert_shamsi_strings_to_datetime(df, config):
    jalali_dates = list()
    sections = df["time"].str.split("-")
    for section in sections:
        right_section = section.pop()
        clean_right_section1 = right_section.strip().split(" ")
        section.append(clean_right_section1[0])
        clean_right_section2 = clean_right_section1[1].strip().split(":")
        section.append(clean_right_section2[0])
        section.append(clean_right_section2[1])
        last_sections = clean_right_section2[2].split(".")
        section.append(last_sections[0])
        section.append(last_sections[1])
        date1 = str((
                        JalaliDatetime(int(section[0]), int(section[1]), int(section[2]), int(section[3]),
                                       int(section[4]),
                                       int(section[5]), int(section[6]))).todatetime()).split("-")
        jalali_dates.append(
            datetime(int(date1[0]), int(date1[1]), int((date1[2].split())[0]), int(section[3]), int(section[4]),
                     int(section[5]), int(section[6])))
    if(config['tool'] == 'Pandas'):
        jalali_Series = pd.Series(jalali_dates)
    if(config['tool'] == 'Dask'):
        jalali_Series_tmp = pd.Series(jalali_dates)
        jalali_Series = dd.from_pandas(jalali_Series_tmp, npartitions=2)
    result = df.assign(time=jalali_Series)
    result.set_index("time")
    return result


def convert_datetime_to_JalaliDatetime(df, config):
    shamsi_dates = list()
    for item in df["time"]:
        shamsi_dates.append(str(JalaliDatetime(item)))
        print(df["time"])
    if(config['tool'] == 'Pandas'):
        shamsi_Series = pd.Series(shamsi_dates)
    elif(config['tool'] == 'Dask'):
        shamsi_Series_tmp = pd.Series(shamsi_dates)
        shamsi_Series = dd.from_pandas(shamsi_Series_tmp, npartitions=2)
    result = df.assign(time=shamsi_Series)
    return result


def interpolate(data, config):
    if (config['interpolation'] == 'linear'):
        return linear_interpolation(data, config)
    elif (config['interpolation'] == 'polynomial'):
        return polynomial_interpolation(data, config)
    elif (config['interpolation'] == 'spline'):
        return spline_interpolation(data, config)


def read_json_time_series(dict_data, config):  # "1399-12-12 15:16:17.101" it is structure of our shamsi dates
    j_data = json.dumps(dict_data)
    data = pd.read_json(j_data)
    if config['tool'] == 'Dask':
        data = dd.from_pandas(data, npartitions=10)
    if config['type'] == 'miladi':
        if config['tool'] == 'Pandas':
            data.time = pd.to_datetime(data.time, unit='ms')
        elif config['tool'] == 'Dask':
            data.time = dd.to_datetime(data.time, unit='ms')
    elif config['type'] == 'shamsi':
        return convert_shamsi_strings_to_datetime(data, config)
    return data
