from flask import Flask, request, jsonify
from utils.common import read_json, response_message, read_json_time_series
from utils.interpolation_methods import *
from utils.outlier_detection import *
from utils.imbalanced_data_handler import *
from flask_swagger_ui import get_swaggerui_blueprint
import pandas as pd

app = Flask(__name__)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

@app.route('/', methods=['GET', 'POST'])
def isup():
    return response_message('API is active')


@app.route('/service1', methods=['GET', 'POST'])
def interpolation():

    req = request.get_json()
    # data = read_json_time_series(req['data'])
    config = req['config']

    if config['type'] == 'miladi':
        data = read_json_time_series(req['data'])
        result = time_series_interpolation(data, config)
        result = result.to_json()
        return response_message({"data": result})

    elif config['type'] == 'shamsi':
        data = read_json(req['data'])
        result = jalali_interpolation(data, config)
        result = result.to_json()
        return response_message({"data": result})


@app.route('/service2', methods=['GET', 'POST'])
def date_converting_and_interpolation():

    req = request.get_json()
    data = read_json_time_series(req['data'])
    config = req['config']

    result = time_series_interpolation(data, config)
    result['time'] = result.time.apply(convert_to_jalali)
    # dropping hodidays
    if config['skip_holiday']:
        result.drop(result.loc[result.time.apply(is_holiday)].index,inplace=True)
        result.reset_index(inplace=True)
    result = result.to_json()
    return response_message({"data": result})


@app.route('/service3', methods=['GET', 'POST'])
def outlier_detection():
    req = request.get_json()
    data = read_json(req['data'])
    config = req['config']

    if config["time_series"]:
        col_name = 'vol'
        id = data['time']
        # method1 for time-series
        outlier_indexes = IsolationForest(data,col_name)
        res1 = set_outlier(data,outlier_indexes,'method1')

        # method2 for time-series
        outlier_indexes = prophet_model(data)
        res2 = set_outlier(data,outlier_indexes,'method2')
        
        result = pd.concat([id,res1,res2],keys=['id','method1','method2'],axis=1)

    else:
        col_name = 'feature'
        id = data['id']
        # method 1
        outlier_indexes = z_score(data,col_name)
        res1 = set_outlier(data,outlier_indexes,'method1')

        # method 2 
        outlier_indexes = IQR(data,col_name)
        res2 = set_outlier(data,outlier_indexes,'method2')

        # method 3 
        outlier_indexes = IsolationForest(data,col_name)
        res3 = set_outlier(data,outlier_indexes,'method3')

        result = pd.concat([id,res1,res2,res3],keys=['id','method1','method2','method3'],axis=1)

   
    result = result.to_json()
    return response_message({"data": result})

@app.route('/service4', methods=['GET', 'POST'])
def imbalance_data():
    req = request.get_json()
    data = read_json(req['data'])
    config = req['config']

    if config['method'] == 'undersampling':
        result = undersampling(data,config["minor_class"],config["major_class"])
        
    elif config['method'] == 'oversampling':
        result = oversampling(data,config["minor_class"],config["major_class"])
        
    elif config['method'] == 'SMOTE':
        result = smote_method(data,config["minor_class"],config["major_class"])

    elif config['method'] == 'Near Miss':
        result = Near_Miss(data,config["minor_class"])

    result = result.reset_index()
    result = result.drop('index',axis=1)
    result = result.to_json()
    
    return response_message({"data": result})





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
