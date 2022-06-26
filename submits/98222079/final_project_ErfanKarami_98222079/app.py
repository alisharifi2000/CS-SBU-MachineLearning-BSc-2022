from flask import Flask, request, jsonify
from utils.common import response_message, read_dataframe_data
from utils.interpolation_methods import interpolation_convert,persian_interpolat
from utils.imbalance_methods import imbalance_manager
from utils.anomaly_detection_methodes import anomaly_detector

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def isup():
    return response_message('API is active')


@app.route('/service1', methods=['GET', 'POST'])
def interpolation():
    req = request.get_json()
    data = req['data']
    data = read_dataframe_data(data)

    config = req['config']

    result=interpolation_convert(data, config)
    result = result.to_json()
    return response_message(dict({"data": result}))


@app.route('/service2', methods=['GET', 'POST'])
def persian_interpolation():
    req = request.get_json()
    data = req['data']
    data = read_dataframe_data(data)

    config = req['config']

    result=persian_interpolat(data, config)
    result = result.to_json()
    return response_message(dict({"data": result}))


@app.route('/service3', methods=['GET', 'POST'])
def anomaly_detection():
    req = request.get_json()
    data = req['data']
    data = read_dataframe_data(data)

    config = req['config']

    result=anomaly_detector(data, config)
    result = result.to_json()
    return response_message(dict({"data": result}))



@app.route('/service4', methods=['GET', 'POST'])
def imbalance_data():
    req = request.get_json()
    data = req['data']
    data = read_dataframe_data(data)

    config = req['config']

    result=imbalance_manager(data, config)
    result = result.to_json()
    return response_message(dict({"data": result}))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
