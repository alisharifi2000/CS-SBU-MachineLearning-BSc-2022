from flask import Flask, request, jsonify, Blueprint
from flask_swagger_ui import get_swaggerui_blueprint
from utils.common import response_message, read_json
from utils.interpolation_methods import interpolate, convert_and_interpolate
from utils.outlier_detection import outlier_detector, outlier_detector_time_series
from utils.imbalance import undersampler, oversampler, smote, near_miss, borderline_smote, svm_smote, adasyn


app = Flask(__name__)


### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Final ML Project Services"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###


app.register_blueprint(Blueprint('request_api', __name__))


@app.route('/', methods=['GET', 'POST'])
def isup():
    return response_message('API is active.')


@app.route('/service1', methods=['GET', 'POST'])
def interpolation():
    req = request.get_json()
    data = read_json(req['data'])
    config = req['config']

    result = interpolate(data, config)

    result = result.to_json()
    return response_message(dict({"data": result}))


@app.route('/service2', methods=['GET', 'POST'])
def conversion_and_interpolation():
    req = request.get_json()
    data = read_json(req['data'])
    config = req['config']

    result = convert_and_interpolate(data, config)
    
    result = result.to_json()
    return response_message(dict({"data": result}))


@app.route('/service3', methods=['GET', 'POST'])
def outlier_detection():
    req = request.get_json()
    data = read_json(req['data'])
    config = req['config']

    if config['time_series'] == False:
        result = outlier_detector(data)
    else:
        result = outlier_detector_time_series(data)
    
    result = result.to_json()
    return response_message(dict({"data": result}))


@app.route('/service4', methods=['GET', 'POST'])
def imbalanced():
    req = request.get_json()
    data = read_json(req['data'])
    config = req['config']

    if config['method'] == "NEARMISS":
        result = near_miss(data)
    elif config['method'] == "OVERSAMPLING":
        result = oversampler(data)
    elif config['method'] == "SMOTE":
        result = smote(data)
    elif config['method'] == "UNDERSAMPLING":
        result = undersampler(data)
    elif config['method'] == "BORDERLINESMOTE":
        result = borderline_smote(data)
    elif config['method'] == "SVMSMOTE":
        result = svm_smote(data)
    elif config['method'] == "ADASYN":
        result = adasyn(data)
    
    result = result.to_json()
    return response_message(dict({"data": result}))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

