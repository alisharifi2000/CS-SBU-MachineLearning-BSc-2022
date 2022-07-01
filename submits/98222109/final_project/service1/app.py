import pandas as pd
from flask import Flask, request
from flasgger import Swagger, swag_from
from utils.common import response_message, read_json_time_series, convert_datetime_to_JalaliDatetime, interpolate
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


@app.route('/service1', methods=['GET', 'POST'])
def interpolation():
    req = request.get_json()
    config = req['config']
    data = read_json_time_series(req['data'], config)

    if config['type'] == 'miladi':
        result = interpolate(data, config)
        result = result.to_json()
    elif config['type'] == 'shamsi':
        result = convert_datetime_to_JalaliDatetime(interpolate(data, config), config)
        result = result.to_json()

    return response_message(dict({"data": result}))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
