from flask import Flask, request
from utils.common import response_message, read_json, combine_results
from utils.anomaly_detection_methods import *
from flasgger import Swagger, swag_from
import config


app = Flask(__name__)
app.config['SWAGGER'] = {
    "specs_route": "/report/"
}
app.config.from_object(config.Config)
swagger = Swagger(app, template_file='report.yml')


@app.route('/', methods=['GET', 'POST'])
def isup():
   return response_message('API is active')


@app.route('/service3', methods=['GET', 'POST'])
def anomaly_detection():
    req = request.get_json()
    config = req['config']
    data = read_json(req['data'], config)
    data_cp = data.copy()

    result1 = isolation_forest(data, config)
    result2 = LOF(data_cp, config)
    final_result = combine_results(result1, result2, config).to_json()
    return response_message(dict({"data": final_result}))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
