from flask import Flask, request, jsonify, make_response, json
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import NearMiss
from flask_swagger_ui import get_swaggerui_blueprint
import gzip
import pandas as pd
import numpy as np
import datetime
import jalali_pandas
from khayyam import JalaliDate, JalaliDatetime
from scipy import stats
from prophet import Prophet

def response_message(data=None, status=200):
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

def interpolate(data, config):
  data.index = data['time']
  del data['time']
  if(config['time'] == 'daily'):
    data = data.resample('D').mean()
  elif(config['time'] == 'monthly'):
    data = data.resample('M').mean()

  if(config['interpolation'] == 'linear'):
    data['vol'] = data['vol'].interpolate()
  elif(config['interpolation'] == 'spline'):
    data['vol'] = data['vol'].interpolate(method = 'spline', order = 2)

  data = data.reset_index()
  
  if(config['skip_holiday']):
    data['weekday'] = data['time'].jalali.to_jalali()
    data['weekday'] = data['weekday'].jalali.weekday
    data.drop(data[data['weekday'] > 4].index, inplace = True)
  if(config['type'] == 'shamsi'):
      data['time'] = data['time'].apply(lambda x : JalaliDate(x).strftime('%Y-%m-%d'))
  return data
  
def outlier(data):
  result = pd.DataFrame({"id":data['id'],"method1": False, "method2": False})
  z = np.abs(stats.zscore(data['feature']))
  result['method1'].values[np.where(z > 3)] = True
  q1 = data['feature'].quantile(0.25)
  q3 = data['feature'].quantile(0.75)
  IQR = q3 - q1
  outliers = data['feature'][((data['feature'] < (q1 - 1.5 * IQR)) | (data['feature'] > (q3 + 1.5 * IQR)))].index
  result['method2'][outliers] = True

  return result

def outlier_time_series(data):
  result = pd.DataFrame({"time":data['time'],"method1": False, "method2": False})

  r = data['vol'].rolling(window = 2)
  mean = r.mean().shift(1)
  std = r.std().shift(1)
  z = (data['vol'] - mean) / std
  result['method1'].values[np.where(z > 3)] = True

  data = data.rename(columns={'time':'ds'})
  data = data.rename(columns={'vol':'y'})
  m = Prophet()
  m.fit(data)
  future = m.make_future_dataframe(periods=50)
  forecast = m.predict(future)
  lower = forecast.yhat_lower.mean()
  upper = forecast.yhat_upper.mean()
  outliers = data['y'][((data['y'] > upper) | (data['y'] < lower))].index
  result['method2'][outliers] = True
  
  return result

def resampling(data, config):
  X = data.drop('class' , axis = 1)
  y = data['class']

  if(config['method'] == "UnderSampling"):
    sampler = RandomUnderSampler()
  elif(config['method'] == "OverSampling"):
    sampler = RandomOverSampler()
  elif(config['method'] == "SMOTE"):
    sampler = SMOTE()
  elif(config['method'] == "NearMiss"):
    sampler = NearMiss()
  X_res, y_res = sampler.fit_resample(X, y)

  result = pd.concat([X_res, y_res], axis = 1)
  return result

app = Flask(__name__)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': ""
    }
)

app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

@app.route('/', methods=['GET', 'POST'])
def isup():
    return response_message('API is active')


@app.route('/service1', methods=['GET', 'POST'])
def interpolation():
    req = request.get_json()
    data = pd.DataFrame(req['data'])

    config = req['config']
    config['skip_holiday'] = False
    
    if(config['type'] == 'shamsi'):
        data['time'] = data['time'].apply(lambda x : JalaliDatetime.strptime(x, '%Y-%m-%d').todatetime())
    else:
        data.time = pd.to_datetime(data.time, unit='ms')
        
    result = interpolate(data, config)
    return response_message(dict({"data": json.loads(result.to_json())}))
    
@app.route('/service2', methods=['GET', 'POST'])
def interpolation2():
    req = request.get_json()
    data = pd.DataFrame(req['data'])
    data.time = pd.to_datetime(data.time, unit='ms')
    config = req['config']
    config['type'] = 'shamsi'
        
    result = interpolate(data, config)
    return response_message(dict({"data": json.loads(result.to_json())}))

@app.route('/service3', methods=['GET', 'POST'])
def outlier_detection():
    req = request.get_json()
    data = pd.DataFrame(req['data'])
    config = req['config']

    if(config['time_series']):
      data.time = pd.to_datetime(data.time, unit='ms')
      result = outlier_time_series(data)
    else:
      result = outlier(data)

    return response_message(dict({"data": json.loads(result.to_json())}))
    
@app.route('/service4', methods=['GET', 'POST'])
def imbalanceManagement():
    req = request.get_json()
    data = pd.DataFrame(req['data'])
    config = req['config']

    result = resampling(data, config)
    return response_message(dict({"data": json.loads(result.to_json())}))
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
