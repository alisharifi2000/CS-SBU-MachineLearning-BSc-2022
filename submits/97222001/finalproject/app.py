from flask import Flask, request, send_from_directory
from services.general import read_jt, read_jn,response
from services.outlier import outlier_finding
from services.imbalaced import balanced_data
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "FinalProject3_Services"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/', methods=['GET', 'POST'])
def isup():
    return response('API is active')


@app.route('/outlier', methods=['GET', 'POST'])
def outlier():
    try:
        req = request.get_json()
        config = req['config']
        data = read_jt(req['data'], False) if config['time_series'] else read_jn(req['data'])

        result = outlier_finding(data, config)

        result = result.to_json()

        return response(dict({"data": result}))
    except Exception as e:
        print(e)

@app.route('/imbal', methods=['GET', 'POST'])
def imbalanced():
    try:
        req = request.get_json()
        config = req['config']
        data = read_jn(req['data'])

        result = balanced_data(data, config)

        result = result.to_json()

        return response(dict({"data": result}))
    except Exception as e:
        print(e)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)