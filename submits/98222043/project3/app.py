from flask import Flask, request, jsonify , make_response
import jalali_pandas
import pandas as pd
import numpy as np
from datetime import date
from khayyam import JalaliDate
import json
import gzip
from prophet import Prophet
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import NearMiss
from flask_swagger_ui import get_swaggerui_blueprint

def response_message(data=None, status=200):
    if status in range(200, 400):
        content = gzip.compress(json.dumps(data, ensure_ascii=False, indent=3, default=convert,
                                           sort_keys=False).encode('utf8'), 5)
    else:
        content = gzip.compress(json.dumps({'message': data, 'status': 'error'}, ensure_ascii=False, indent=3).encode('utf-8'), 5)
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

def interpolation1(df , config):
  config_time = config['time']
  config_inter = config['interpolation']
  config_type = config['type']

  resample_freq = 'D'
  if config_time == 'monthly' :
    resample_freq = 'M'

  shamsi = False
  if config_type == 'shamsi' :
    df.time  = df['time'].jalali.to_gregorian()
    shamsi = True

  df.index = df['time']
  del df['time']
  df_interpol = df.resample(resample_freq).mean()
  df_interpol['vol'] = df_interpol['vol'].interpolate(method = 'linear')
  df_interpol = df_interpol.reset_index()

  if shamsi == True :
    #convert
    df_interpol.time  = df_interpol['time'].apply(lambda x : JalaliDate(x).strftime('%Y/%m/%d'))
  return df_interpol

def interpolation2(df , config):
  config_time = config['time']
  config_inter = config['interpolation']
  config_skipHoli = config['skip_holiday']

  resample_freq = 'D'
  if config_time == 'monthly' :
    resample_freq = 'M'

  skipH = False
  if config_skipHoli == True :
    skipH = True

  df.index = df['time']
  del df['time']

  df_interpol = df.resample(resample_freq).mean()
  df_interpol['vol'] = df_interpol['vol'].interpolate(method = 'linear')
  df_interpol = df_interpol.reset_index()

  df_interpol['weekday'] = df_interpol['time'].jalali.to_jalali().jalali.weekday

  if skipH :
    values = [5,6]
    df_interpol = df_interpol[df_interpol.weekday.isin(values) == False]
  

  df_interpol.drop('weekday', axis=1, inplace=True)
  df_interpol.time  = df_interpol['time'].apply(lambda x : JalaliDate(x).strftime('%Y/%m/%d'))

  return df_interpol


def outlierdetect1(df):
  result_df = pd.DataFrame(columns = ['id' , 'method1' , 'method2'] , index = range(len(df)))
  result_df['id'] = df['id'].values
  result_df[['method1' , 'method2']] = 'false'

  #method1 : IQR
  Q1 = df['feature'].quantile(0.2)
  Q3 = df['feature'].quantile(0.8)
  IQR = Q3 - Q1
  id = df[(df['feature'] < (Q1 - 1.5 * IQR)) | (df['feature'] > (Q3 + 1.5 * IQR))].id
  result_df.loc[id - 1 , 'method1'] = 'true'
  
  #method2 : z-score
  mean = np.mean(df['feature'])
  std = np.std(df['feature'])
  threshold = 3
  id = df[ ((df['feature'] - mean)/std) > threshold].id
  result_df.loc[id - 1 , 'method2'] = 'true'  
  
  return result_df


def outlierdetect2(tdf):
  result_df = pd.DataFrame(columns = ['time' , 'method1' , 'method2'] , index = range(len(tdf)))
  result_df['time'] = tdf['time'].values
  result_df[['method1' , 'method2']] = 'false'

  #method1 : z-score
  window = 2
  r = tdf['vol'].rolling(window=window)
  mean = r.mean().shift(1)
  std = r.std().shift(1)
  z = (tdf['vol']-mean)/std
  for i in range(len(z)):
    if z[i] > 3 : 
      result_df.loc[i , 'method1'] = 'true'

  #method2 : prophet
  tdf = tdf.rename(columns={'time':'ds'})
  tdf = tdf.rename(columns={'vol':'y'})
  m = Prophet()
  m.fit(tdf)
  future = m.make_future_dataframe(periods=50)
  forecast = m.predict(future)
  lower = forecast.yhat_lower.mean()
  upper = forecast.yhat_upper.mean()
  for i in range(len(tdf)):
    if ((tdf.y[i] > upper) | (tdf.y[i] < lower)) : 
      result_df.loc[i , 'method2'] = 'true'

  return result_df

def imbalancedfix(df , config):
  result = []
  X = df.drop(['class'], axis=1)
  y = df['class']

  if config['method'] == "SMOTE":
    major = config['major_class']
    minor = config['minor_class']
    count = df['class'].value_counts()[major]
    smotesampler = SMOTE(k_neighbors=1 , sampling_strategy = {minor : count} )
    X_smote, y_smote = smotesampler.fit_resample(X, y)
    result = X_smote.join(y_smote)

  elif config['method'] == "oversampling":
    oversample = RandomOverSampler(sampling_strategy=0.6)
    X_over, y_over = oversample.fit_resample(X, y)
    result = X_over.join(y_over)

  elif config['method'] == "undersampling":
    undersample = RandomUnderSampler(sampling_strategy=0.5)
    X_under, y_under = undersample.fit_resample(X, y)
    result = X_under.join(y_under)

  elif config['method'] == "nearmiss":
    nmundersample = NearMiss(version=1, n_neighbors=2)
    X_near, y_near = nmundersample.fit_resample(X, y)
    result = X_near.join(y_near)


  return result

#//////

app = Flask(__name__)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
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

#////// 

#1
@app.route('/service1', methods=['GET', 'POST'])
def main1():
  req = request.get_json()
  data_df = pd.DataFrame(req['data'])
  config = req['config']
  if config['type'] == 'shamsi':
    data_df.time = data_df["time"].jalali.parse_jalali("%Y/%m/%d")
  else:
    data_df.time = pd.to_datetime(data_df.time, unit='ms')

  result = interpolation1(data_df, config)
  return response_message(dict({"data": json.loads(result.to_json())}))

#2
@app.route('/service2', methods=['GET', 'POST'])
def main2():
  req = request.get_json()
  data_df = pd.DataFrame(req['data'])
  config = req['config']

  data_df.time = pd.to_datetime(data_df.time, unit='ms')

  result = interpolation2(data_df, config)
  return response_message(dict({"data": json.loads(result.to_json())}))

#3
@app.route('/service3', methods=['GET', 'POST'])
def main3():
  req = request.get_json()
  data_df = pd.DataFrame(req['data'])
  config = req['config']
  if config['time_series'] == False:
    result = outlierdetect1(data_df)
  elif config['time_series'] == True:
    data_df.time = pd.to_datetime(data_df.time, unit='ms')
    result = outlierdetect2(data_df)
    
  return response_message(dict({"data": json.loads(result.to_json())}))

#4
@app.route('/service4', methods=['GET', 'POST'])
def main4():
  req = request.get_json()
  data_df = pd.DataFrame(req['data'])
  config = req['config']

  result = imbalancedfix(data_df, config)
  return response_message(dict({"data": json.loads(result.to_json())}))

#////////


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
