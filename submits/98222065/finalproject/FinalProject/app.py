import numpy as np
import pandas as pd
from flask import Flask, request

from utils.balancing_methods import *
from utils.common import *
from utils.interpolation_methods import *
from utils.outlier_finder_methods import *

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def isup():
    return "API is active!"


@app.route("/service1", methods=["GET", "POST"])
def time_interpolation():
    req = request.get_json()
    config = req["config"]
    data = read_json_time_series(req["data"], config["type"])
    result = interpolation(data, config)
    if config["type"] == "shamsi":
        result = miladi_to_shamsi(result)
    return return_data(result.to_json())

@app.route("/service2", methods=["GET", "POST"])
def time_interpolation_miladi_to_shamsi():
    req = request.get_json()
    config = req["config"]
    data = read_json_time_series(req["data"], "miladi")
    result = interpolation(data, config)    
    result = miladi_to_shamsi(result)
    return return_data(result.to_json())

@app.route("/service3", methods=["GET", "POST"])
def outlier_data():
    req = request.get_json()
    config = req["config"]
    if config["time_series"]:
        data = read_time_series(req["data"])
        quantile = find_outliers_using_quantile(data)
        method1 = quantile["feature"]
        # method2 = find_outliers_using_z_score(data)      
    else:
        data = json_to_panda(req["data"])
        quantile = find_outliers_using_quantile(data)
        method1 = quantile["feature"]
        # method2 = find_outliers_using_z_score(data)
    result = {"method1": method1, "method2": method1}
    result = pd.DataFrame(result)
    return return_data(result.to_json())    

@app.route('/service4', methods=['GET', 'POST'])
def imbalance_data():
    req = request.get_json()
    data = pd.DataFrame(req['data'])
    config = req['config']

    result = balancing(data, config)
    return return_data(result.to_json())
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
