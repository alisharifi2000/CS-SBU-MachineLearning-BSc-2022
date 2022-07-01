from calendar import monthrange
import gzip
from traceback import print_tb
from flask import make_response, json
import pandas as pd
import numpy as np
import json
import datetime
import jdatetime
from .interpolation_methods import interpolation
from .outlier_detection import anomoly_detection, outlier_detection
from adtk.data import validate_series
from .imbalanced import balance_imbalanced
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


def read_json_time_series(dict_data,config):
    if config.get("type",None) == None:
        config["type"] = "gregorian"
    if config["type"] == "gregorian":
        if config["time"] == "monthly":
            for x in dict_data["time"].keys():
                year_month = dict_data["time"][x].split("-")
                end_month = monthrange(int(year_month[0]), int(year_month[1]))
                month = datetime.datetime(year = int(year_month[0]),month= int(year_month[1]),day=end_month[1])
                dict_data["time"][x] = month.__str__()
        else:
            for x in dict_data["time"].keys():
                dict_data["time"][x] = datetime.datetime.strptime(dict_data["time"][x],"%Y-%m-%d %H:%M:%S").__str__()
    else:
        if config["time"] == "monthly":
            for x in dict_data["time"].keys():
                year_month = dict_data["time"][x].split("-")
                end_month = monthrange(int(year_month[0]), int(year_month[1]))
                month = datetime.datetime(year = int(year_month[0])+600,month= int(year_month[1]),day=end_month[1])
                dict_data["time"][x] = month.__str__()
        else:
            for x in dict_data["time"].keys():
                mydate = jdatetime.datetime.strptime(dict_data["time"][x],"%Y-%m-%d %H:%M:%S")
                dict_data["time"][x] = mydate.togregorian().__str__()
    j_data = json.dumps(dict_data)
    data = pd.read_json(j_data)
    data.time = pd.to_datetime(data.time)
    return data

def read_json(data, config):
    j_data = json.dumps(data)
    data = pd.read_json(j_data)
    return data

def config_final_result(result, config):
    if config["type"] == "gregorian":
        result = json.loads(result)
        if config["time"] == "monthly":
            for x in result.keys():
                mydate = datetime.datetime.strptime(result[x]["time"],"%Y-%m-%dT%H:%M:%SZ")
                final_date = str(mydate.year) + "-"
                if mydate.month < 10:
                    final_date = final_date +"0"+ str(mydate.month)
                else:
                    final_date = final_date +str(mydate.month)
                result[x]["time"] = final_date
        return result
    else:
        result = json.loads(result)
        if config["time"] == "monthly":
            for x in result.keys():
                mydate = datetime.datetime.strptime(result[x]["time"],"%Y-%m-%dT%H:%M:%SZ")
                final_date = (mydate.year-600)
                final_date = str(final_date) + "-"
                if mydate.month < 10:
                    final_date = final_date +"0"+ str(mydate.month)
                else:
                    final_date = final_date +str(mydate.month)
                result[x]["time"] = final_date
        else:
            for x in result.keys():
                mydate = datetime.datetime.strptime(result[x]["time"],"%Y-%m-%dT%H:%M:%SZ")
                jdate = jdatetime.datetime.fromgregorian(datetime = mydate)
                result[x]["time"] = jdate.__str__()
        return result

def gregorian_to_jalali(result, config):
    result = json.loads(result)
    if config["time"] == "monthly":
        for x in result.keys():
            mydate = datetime.datetime.strptime(result[x]["time"],"%Y-%m-%dT%H:%M:%SZ")
            jalali_date = jdatetime.datetime.fromgregorian(datetime = mydate)
            final_date = str(jalali_date.year) + "-"
            if jalali_date.month < 10:
                final_date = final_date +"0"+ str(mydate.month)
            else:
                final_date = final_date +str(mydate.month)
            result[x]["time"] = final_date
    else:
        for x in result.keys():
            mydate = datetime.datetime.strptime(result[x]["time"],"%Y-%m-%dT%H:%M:%SZ")
            jdate = jdatetime.datetime.fromgregorian(datetime = mydate)
            result[x]["time"] = jdate.__str__()
    return result

def read_and_anomoly_detection(data, config):
    if config['time_series']:
        config["time"] = "daily"
        config["interpolation"] = "linear"
        config["order"] = 3
        df = read_json_time_series(data, config)
        df  = interpolation(df,config)
        df = validate_series(df)
        return anomoly_detection(df,config)
    else:
        df = read_json(data, config)
        return outlier_detection(df,config)

def split_X_y(df:pd.DataFrame, config):
    class_name = config["class_name"]
    y = df[class_name]
    df.drop(class_name,axis=1,inplace=True)
    return df, y

def read_and_balance(data, config):
    df = read_json(data,config)
    print(df)
    X,y = split_X_y(df,config)
    print(X, "....................")
    print(y,"adasdsdsddassdasdas")
    balanced_df = balance_imbalanced(X,y,config)
    final_result = balanced_df.to_json(orient='index')
    final_result = json.loads(final_result)
    return final_result
