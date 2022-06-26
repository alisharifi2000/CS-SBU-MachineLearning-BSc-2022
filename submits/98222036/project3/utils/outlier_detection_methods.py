from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest
from pyod.models.abod import ABOD

z_score_threshold = 3
local_outlier_factor_n_neighbors = 2
local_outlier_factor_metric = 'manhattan'
isolation_forest_n_estimators = 10
abod_contamination = 0.1
abod_method = 'fast'
abod_n_neighbors = 2

def iqr_detector(data, index_col, val_col):
    percentile25 = data[val_col].quantile(0.25)
    percentile75 = data[val_col].quantile(0.75)
    iqr = percentile75 - percentile25
    upper_limit = percentile75 + 1.5 * iqr
    lower_limit = percentile25 - 1.5 * iqr
    return (data[val_col] < lower_limit) | (data[val_col] > upper_limit)

def z_score_detector(data, index_col, val_col):
    mean = data[val_col].mean()
    std = data[val_col].std()
    return (((data[val_col] - mean)/std) > z_score_threshold)

def local_outlier_factor_detector(data, index_col, val_col):
    lof = LocalOutlierFactor(n_neighbors=local_outlier_factor_n_neighbors, metric=local_outlier_factor_metric, n_jobs=-1)
    pred = lof.fit_predict([data[val_col]])
    return (pred != 1)

def isolation_forest_detector(data, index_col, val_col):
    isf = IsolationForest(n_estimators=isolation_forest_n_estimators, n_jobs=-1)
    isf.fit([data[val_col]])
    pred = isf.predict([data[val_col]])
    return (pred != 1)

def abod_detector(data, index_col, val_col):
    abod_model = ABOD(contamination=abod_contamination, method=abod_method, n_neighbors=abod_n_neighbors)
    abod_model.fit([data[val_col]])
    pred = abod_model.predict([data[val_col]])
    return (pred != 0)

normal_detectors = {
    'IQR':iqr_detector, 
    'z_score':z_score_detector, 
    'local_outlier_factor':local_outlier_factor_detector, 
    'isolation_forest':isolation_forest_detector, 
    'ABOD':abod_detector
    }

time_seri_detectors = {
    'IQR':iqr_detector, 
    'z_score':z_score_detector, 
    'local_outlier_factor':local_outlier_factor_detector, 
    'isolation_forest':isolation_forest_detector, 
    'ABOD':abod_detector
    }

def outlier_detection(data, config):
    try:
        if (config['time_series']):
            for name, func in time_seri_detectors.items():
                data[name] = func(data, 'time', 'vol')
            data.drop(['vol'], axis=1, inplace=True)
        else:
            for name, func in normal_detectors.items():
                data[name] = func(data, 'id', 'feature')
            data.drop(['feature'], axis=1, inplace=True)
    except Exception as e:
        raise e

    return data

"""
{
  "data": {
    "id": {
      "0": 1,
      "1": 2,
      "2": 3,
      "3": 4,
      "4": 5,
      "5": 6
    },
    "feature": {
      "0": 100,
      "1": 20,
      "2": 35,
      "3": 67,
      "4": 89,
      "5": 90
    }
  },
  "config": {
    "time_series": false
  }
}


{
  "data": {
    "time": {
      "0": 1,
      "1": 2,
      "2": 3,
      "3": 4,
      "4": 5,
      "5": 6
    },
    "vol": {
      "0": 100,
      "1": 20,
      "2": 35,
      "3": 67,
      "4": 89,
      "5": 90
    }
  },
  "config": {
    "time_series": false
  }
}
"""
