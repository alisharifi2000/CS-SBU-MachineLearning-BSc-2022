
import numpy as np
import pandas as pd
from flask import Flask, request
from khayyam import JalaliDatetime
from scipy import stats

from utils.balancing_methods import balancing
from utils.common import json_to_panda, read_json_time_series, read_time_series
from utils.interpolation_methods import interpolation

app = Flask(__name__)

@app.route("/v1/", methods=["GET"])
def isup():
    return "You have 4 services available."


@app.route("/v1/service1", methods=["POST"])
def time_interpolation():
    req = request.get_json()
    config = req["config"]
    data = read_json_time_series(req["data"], config["type"])
    result = interpolation(data, config)
    if config["type"] == "shamsi":
        for _ in range(len(result["time"])):
            result["time"][_] = JalaliDatetime(result["time"][_]).isoformat()

    return result.to_json()

@app.route("/v1/service2", methods=["GET", "POST"])
def time_interpolation_miladi_to_shamsi():
    req = request.get_json()
    config = req["config"]
    data = read_json_time_series(req["data"], "miladi")
    result = interpolation(data, config)
    for _ in range(len(result["time"])):
        result["time"][_] = JalaliDatetime(result["time"][_]).isoformat()

    return result.to_json()

@app.route("/v1/service3", methods=["POST"])
def find_outliers():
    req = request.get_json()
    config = req["config"]
    if config["time_series"]:
        data = read_time_series(req["data"])
        q = np.logical_or(data > data.quantile(0.75),
                     data < data.quantile(0.25))
        method1 = q["feature"]
        # z = np.abs(stats.zscore(data.feature))
        # method2 = z.gt(3)
        result = {"method1": method1, "method2": method1}
        df=pd.DataFrame(result)
        return df.to_json()
            
    else:
        data = json_to_panda(req["data"])
        z = np.abs(stats.zscore(data['feature']))
        method1 = z.gt(3)
        q = np.logical_or(data > data.quantile(0.9),
                     data < data.quantile(0.1))
        method2 = q["feature"]
        result = {"method1": method1, "method2": method2}
        df=pd.DataFrame(result)
        return df.to_json()

@app.route('/v1/service4', methods=['POST'])
def imbalance_data():
    req = request.get_json()
    data = pd.DataFrame(req['data'])
    config = req['config']

    result = balancing(data, config)
    return result.to_json()
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
