from flask import Flask, request
from utils.common import response_message, read_json_time_series, read_json_simple
from utils.interpolationMethods import linear_interpolation , toShamsi , linear_interpolation2
from utils.outlierMethods import zscore,IQR,isolationForest , dbscan , isolationForestTime
from utils.unbalancedDataMethods import smote , oversampling ,undersampling,tomekLinksUndersamplingFunc
import pandas as pd


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def isup():
    return response_message('API is active')

@app.route('/service1', methods=['GET', 'POST'])
def interpolation():
    req = request.get_json()

    data = read_json_simple(req['data'])
    config = req['config']

    if config['type'] == 'miladi':
        data.time = pd.to_datetime(data.time, unit='ms')


    result = linear_interpolation(data, config)

    result = result.to_json()
    return response_message(dict({"data": result}))




@app.route('/service2', methods=['GET', 'POST'])
def shamsiInterpolation():
    req = request.get_json()
    data = read_json_time_series(req['data'])
    config = req['config']

    result = linear_interpolation2(data, config)
    result2 = toShamsi(result)
    result2 = result2.to_json()
    print(result2)

    return response_message(dict({"data": result2}))



@app.route('/service3', methods=['GET', 'POST'])
def outlierDetect():
    req = request.get_json()
    data = read_json_simple(req['data'])
    config = req['config']

    if config['time_series'] == True:
        data.time = pd.to_datetime(data.time, unit='ms')
        result = isolationForestTime(data)
        result = dbscan(result)

        result = result.to_json()
        return response_message(dict({"data": result}))

    elif config['time_series'] == False:
        result = zscore(data, config)
        result = IQR(result, config)
        result = isolationForest(result)

        result = result.to_json()
        return response_message(dict({"data": result}))






@app.route('/service4', methods=['GET', 'POST'])
def unbalancedData():
    req = request.get_json()
    data = read_json_simple(req['data'])
    config = req['config']

    if config['method'] == 'SMOTE':
        result = smote(data, config)
        result = result.to_json()
        return response_message(dict({"data": result}))
    elif config['method'] == 'oversampling' :
        result = oversampling(data, config)
        result = result.to_json()
        return response_message(dict({"data": result}))
    elif config['method'] == 'undersampling' :
        result = undersampling(data, config)
        result = result.to_json()
        return response_message(dict({"data": result}))
    elif config['method'] == 'tomeklinks':
        result = tomekLinksUndersamplingFunc(data, config)
        result = result.to_json()
        return response_message(dict({"data": result}))



if __name__ == '__main__':
    app.run()
