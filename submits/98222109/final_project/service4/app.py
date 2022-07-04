from flask import Flask, request
from utils.common import response_message, read_json, cleaning_result
from utils.functions import *
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


@app.route('/service4', methods=['GET', 'POST'])
def imbalance_correcting():
    req = request.get_json()
    config = req['config']
    data = read_json(req['data'])

    if(config['method'] == "SMOTE"):
        result = smote(data)
        cleaning_result(result)
        result = result.to_json()
    elif(config['method'] == "RANDOM_OVERSAMPLING"):
        result = random_oversampling(data)
        cleaning_result(result)
        result = result.to_json()
    elif(config['method'] == "RANDOM_UNDERSAMPLING"):
        result = random_undersampling(data)
        cleaning_result(result)
        result = result.to_json()


    return response_message(dict({"data": result}))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
