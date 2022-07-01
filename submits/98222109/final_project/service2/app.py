from flask import Flask, request
from utils.common import response_message, read_json_time_series, convert_datetime_to_JalaliDatetime, skip_holidays, interpolate
from utils.interpolation_methods import linear_interpolation
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


@app.route('/service2', methods=['GET', 'POST'])
def interpolation():
    req = request.get_json()
    config = req['config']
    data = read_json_time_series(req['data'], config)

    result = convert_datetime_to_JalaliDatetime(interpolate((skip_holidays(data, config)), config), config)
    return response_message(dict({"data": result.to_json()}))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
