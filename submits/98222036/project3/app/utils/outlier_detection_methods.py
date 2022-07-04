from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest
#from pyod.models.abod import ABOD
from sklearn.svm import OneClassSVM
from sklearn.cluster import DBSCAN

z_score_threshold = 3
local_outlier_factor_n_neighbors = 2
local_outlier_factor_metric = 'manhattan'
isolation_forest_n_estimators = 10
isolation_forest_contamination = 'auto'
one_class_svm_kernel = 'rbf'
one_class_svm_max_iter = 1000
one_class_svm_tol = 0.001
one_class_svm_nu = 0.5
dbscan_metric = 'manhattan'
dbscan_eps = 0.8
dbscan_min_samples = 3
#abod_contamination = 0.1
#abod_method = 'fast'
#abod_n_neighbors = 5

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
    pred = lof.fit_predict(data[val_col].values.reshape(-1, 1))
    return (pred != 1)

def isolation_forest_detector(data, index_col, val_col):
    isf = IsolationForest(n_estimators=isolation_forest_n_estimators, contamination=isolation_forest_contamination, n_jobs=-1)
    isf.fit(data[val_col].values.reshape(-1, 1))
    pred = isf.predict(data[val_col].values.reshape(-1, 1))
    return (pred != 1)

def one_class_svm_detector(data, index_col, val_col):
    model = OneClassSVM(kernel=one_class_svm_kernel, tol=one_class_svm_tol, max_iter=one_class_svm_max_iter, nu=one_class_svm_nu)
    pred = model.fit_predict(data[val_col].values.reshape(-1, 1))
    return (pred == -1)

def dbscan_detector(data, index_col, val_col):
    clusters = DBSCAN(eps=dbscan_eps, metric=dbscan_metric, min_samples=dbscan_min_samples ,n_jobs=-1).fit(data[val_col].values.reshape(-1, 1))
    labels = clusters.labels_
    return (labels == -1)

# def abod_detector(data, index_col, val_col):
#     abod_model = ABOD(contamination=abod_contamination, method=abod_method, n_neighbors=abod_n_neighbors)
#     abod_model.fit(data[val_col].values.reshape(-1, 1))
#     pred = abod_model.predict(data[val_col].values.reshape(-1, 1))
#     return (pred != 0)

normal_detectors = {
    'IQR':iqr_detector, 
    'z_score':z_score_detector, 
    'local_outlier_factor':local_outlier_factor_detector, 
    'isolation_forest':isolation_forest_detector, 
    'one_class_svm':one_class_svm_detector
    #'ABOD':abod_detector
    }

time_seri_detectors = {
    'isolation_forest':isolation_forest_detector, 
    'DBSCAN':dbscan_detector
    }

def set_hyper_params(config):
  if ('z_score' in config):
    if ('threshold' in config['z_score']):
      global z_score_threshold
      z_score_threshold = config['z_score']['threshold']
  if ('lof' in config):
    if ('n_neighbors' in config['lof']):
      global local_outlier_factor_n_neighbors
      local_outlier_factor_n_neighbors = config['lof']['n_neighbors']
    if ('metric' in config['lof']):
      global local_outlier_factor_metric
      local_outlier_factor_metric = config['lof']['metric']
  if ('isolation_forest' in config):
    if ("contamination" in config['isolation_forest']):
      global isolation_forest_contamination
      isolation_forest_contamination = config['isolation_forest']['contamination']
    if ("n_estimators" in config['isolation_forest']):
      global isolation_forest_n_estimators
      isolation_forest_n_estimators = config['isolation_forest']['n_estimators']
  if ('one_class_svm' in config):
    if ('kernel' in config['one_class_svm']):
      global one_class_svm_kernel
      one_class_svm_kernel = config['one_class_svm']['kernel']
    if ('max_iter' in config['one_class_svm']):
      global one_class_svm_max_iter
      one_class_svm_max_iter = config['one_class_svm']['max_iter']
    if ('tol' in config['one_class_svm']):
      global one_class_svm_tol
      one_class_svm_tol = config['one_class_svm']['tol']
    if ('nu' in config['one_class_svm']):
      global one_class_svm_nu
      one_class_svm_nu = config['one_class_svm']['nu']
  if ('dbscan' in config):
    if ('metric' in config['dbscan']):
      global dbscan_metric
      dbscan_metric = config['dbscan']['metric']
    if ('eps' in config['dbscan']):
      global dbscan_eps
      dbscan_eps = config['dbscan']['eps']
    if ('min_samples' in config['dbscan']):
      global dbscan_min_samples
      dbscan_min_samples = config['dbscan']['min_samples']

def outlier_detector(data, config):
  try:
      set_hyper_params(config)
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
