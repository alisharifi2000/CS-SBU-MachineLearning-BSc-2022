from flask import Flask, request
from utils.common import response_message, read_json_time_series
from utils.interpolation_methods import interpolate
from khayyam import JalaliDatetime, JalaliDate

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def isup():
    return response_message('API is active')


@app.route('/service1', methods=['GET', 'POST'])
def interpolation():
    try:
        req = request.get_json()
        config = req['config']
        data = read_json_time_series(req['data'], config['type'] == 'shamsi')

        result = interpolate(data, config)

        if config['type'] == 'shamsi':
            result.time = result.time.map(lambda d: JalaliDatetime(d).strftime('%Y-%m-%d-%H-%M-%S-%f'))
        # print(result)
        result = result.to_json()
        # print(result)

        return response_message(dict({"data": result}))
    except Exception as e:
        # print(e)
        return response_message(dict({"data":"400 Bad Request"}), status=400)

@app.route('/service2', methods=['GET', 'POST'])
def shamsiInterpolation():
    try:
        req = request.get_json()
        config = req['config']
        data = read_json_time_series(req['data'], False)
        # print(data.time.map(lambda d: JalaliDatetime(d).strftime('%Y-%m-%d-%H-%M-%S-%f')))

        result = interpolate(data, config)

        # for i in result.time:
            # print(i)
            # print(JalaliDatetime(i).localdatetimeformatascii())

        result.time = result.time.map(lambda d: JalaliDatetime(d).strftime('%Y-%m-%d-%H-%M-%S-%f'))
        # print(result)
        result = result.to_json()
        # print(result)

        return response_message(dict({"data": result}))
    except Exception as e:
        print(e)
        return response_message(dict({"data":"400 Bad Request"}), status=400)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
