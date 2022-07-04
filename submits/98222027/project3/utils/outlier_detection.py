from prophet import Prophet
import numpy as np
import pandas as pd
# z-score method
def z_score(df,col_name):
 
  upper = df[col_name].mean() + 3 * df[col_name].std()
  lower = df[col_name].mean() - 3 * df[col_name].std()

  indexes = df[(df[col_name] > upper) | (df[col_name] < lower)].index
  return indexes

# IQR method
def IQR(df,col_name):

  q1 = np.percentile(df[col_name],25)
  q3 = np.percentile(df[col_name],75)
  iqr = q3 - q1
  lower = q1 - 1.5 * iqr
  upper = q3 + 1.5 * iqr
  indexes = df[(df[col_name] > upper) | (df[col_name] < lower)].index
  return indexes

# IsolationForest 
def IsolationForest(df,col_name):
    from sklearn.ensemble import IsolationForest
    model= IsolationForest()
    model.fit(df[[col_name]])
    prediction = model.predict(df[[col_name]])
    indexes = np.where(prediction<1)[0]
    return indexes

# for time-series outlier detection
def prophet_model(data):
  data.time=pd.to_datetime(data.time,unit='ms')
  data = data.rename(columns={'time':'ds','vol':'y'})
  m = Prophet(daily_seasonality = True, yearly_seasonality = False, weekly_seasonality = False,changepoint_range=0.95)
  m.fit(data)
  prediction = m.predict(data)
  prediction = prediction[['ds','yhat','yhat_lower','yhat_upper']]
  result = pd.concat([prediction,data.y],axis=1)
  result['error'] = result['y'] - result['yhat']
  result['uncertainty'] = result['yhat_upper'] - result['yhat_lower']
  indexes = result[result['error'].abs()> 1.5*result['uncertainty']].index
  return indexes


def set_outlier(df,outlier_indexes,method):
    list = [False] * len(df)
    for idx in outlier_indexes:
        list[idx] = True
    
    return pd.Series(list)
