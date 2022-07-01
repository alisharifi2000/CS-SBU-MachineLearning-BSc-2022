from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM


local_metric = 'manhattan'
local_neighbors = 2
z_threshold = 3
isolation_estimators = 10
isolation_contamination = 'auto'
svm_nu = 0.5
svm_max_iter = 1000
svm_tol = 0.001
svm_kernel = 'rbf'

def z_finder(data, index_col, val_col):
    average = data[val_col].mean()
    std = data[val_col].std()
    return (((data[val_col] - average)/std) > z_threshold)

def svm_finder(data, index_col, val_col):
    m = OneClassSVM(kernel=svm_kernel, tol=svm_tol, max_iter=svm_max_iter, nu=svm_nu)
    p = m.fit_predict(data[val_col].values.reshape(-1, 1))
    return (p == -1)

def isolation_finder(data, index_col, val_col):
    i = IsolationForest(n_estimators=isolation_estimators, contamination=isolation_contamination, n_jobs=-1)
    i.fit(data[val_col].values.reshape(-1, 1))
    p = i.predict(data[val_col].values.reshape(-1, 1))
    return (p != 1)

def satistic_finder(data, index_col, val_col):
    p25 = data[val_col].quantile(0.25)
    p75 = data[val_col].quantile(0.75)
    i = p75 - p25
    upper = p75 + 1.5 * i
    lower = p25 - 1.5 * i
    return (data[val_col] < lower) | (data[val_col] > upper)

def local_finder(data, index_col, val_col):
    l = LocalOutlierFactor(n_neighbors=local_neighbors, metric=local_metric, n_jobs=-1)
    p = l.fit_predict(data[val_col].values.reshape(-1, 1))
    return (p != 1)

time_seri_finder = {
    'isolation':isolation_finder,
    }

normal_finder = {
    'satistic':satistic_finder,
    'z':z_finder,
    'local':local_finder,
    'isolation':isolation_finder,
    'svm':svm_finder
    }

def set_params(config):
  if ('z' in config):
    if ('threshold' in config['z']):
      global z_threshold
      z_threshold = config['z']['threshold']
  if ('svm' in config):
    if ('kernel' in config['svm']):
      global svm_kernel
      svm_kernel = config['svm']['kernel']
    if ('max_iter' in config['svm']):
      global svm_max_iter
      svm_max_iter = config['svm']['max_iter']
    if ('tol' in config['svm']):
      global svm_tol
      svm_tol = config['svm']['tol']
    if ('nu' in config['svm']):
      global svm_nu
      svm_nu = config['svm']['nu']
  if ('lof' in config):
    if ('n_neighbors' in config['lof']):
      global local_neighbors
      local_neighbors = config['lof']['n_neighbors']
    if ('metric' in config['lof']):
      global local_metric
      local_metric = config['lof']['metric']
  if ('isolation' in config):
    if ("contamination" in config['isolation']):
      global isolation_contamination
      isolation_contamination = config['isolation']['contamination']
    if ("n_estimators" in config['isolation']):
      global isolation_estimators
      isolation_estimators = config['isolation']['n_estimators']



def outlier_finding(data, config):
  try:
      set_params(config)
      if (config['time_series']):
          for name, functio in time_seri_finder.items():
              data[name] = functio(data, 'time', 'vol')
          data.drop(['vol'], axis=1, inplace=True)
      else:
          for name, functio in normal_finder.items():
              data[name] = functio(data, 'id', 'feature')
          data.drop(['feature'], axis=1, inplace=True)
  except Exception as e:
      raise e

  return data