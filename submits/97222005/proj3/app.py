from flask import Flask, request, make_response
import json
import pandas as pd
import numpy as np
import gzip
from utils.date_conversion import date_conversion
from utils.interpolation_methods import linear_interpolation
from utils.outlier import OutlierDetector
from utils.balance import BalancerRegistry

app = Flask(__name__)


def response_message(data=None, status=200):
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


def get_data_and_config(request):
    req = request.get_json()
    data = pd.DataFrame(req['data'])
    config = pd.Series(req['config'])
    return data, config


@app.route('/interpolation', methods=['GET', 'POST'])
def interpolation():
    data, config = get_data_and_config(request)
    out = linear_interpolation(data, config)
    return response_message(out)


@app.route('/interpolation_with_date_conversion', methods=['GET', 'POST'])
def interpolation_with_date_conversion():
    data, config = get_data_and_config(request)
    out = date_conversion(data, config)
    return response_message(out)


@app.route('/outlier_detection', methods=['GET', 'POST'])
def outlier_detection():
    data, config = get_data_and_config(request)
    df = OutlierDetector(data,config).run()
    out = df.reset_index().to_json()
    return response_message({'data': out})


@app.route('/imbalanced_data_management', methods=['GET', 'POST'])
def imbalanced_data_management():
    data, config = get_data_and_config(request)
    try:
        balancer = BalancerRegistry.get_instance().get(name=config.method)(data)
        out = {'data': balancer.balance().reset_index().to_json()}
    except NotImplementedError:
        return 'Method Not found', 404
    return response_message(out)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
