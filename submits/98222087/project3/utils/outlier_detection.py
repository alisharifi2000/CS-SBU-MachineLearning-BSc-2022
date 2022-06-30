from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.covariance import EllipticEnvelope
from sklearn.svm import OneClassSVM
from statsmodels.tsa.seasonal import STL
import numpy as np
import pandas as pd
import sesd


def isolation_forest(data):
    iso = IsolationForest(contamination=0.1)
    y_hat = iso.fit_predict(data)
    return y_hat

def local_outlier_factor(data):
    lof = LocalOutlierFactor()
    y_hat = lof.fit_predict(data)
    return y_hat

def iqr(data):
    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
    IQR = q3 - q1
    return (data < q1 - 1.5 * IQR) | (data > q3 + 1.5 * IQR)

def hampel(data):
    med = data.median()
    lis = abs(data - med)
    cond = lis.median() * 4.5
    return (data > cond)

def z_score(data):
    mu = data.mean()
    std = data.std()
    return (abs(data - mu) / std > 1.5)

def mcd(data):
    ee = EllipticEnvelope(contamination=0.01)
    y_hat = ee.fit_predict(data)
    return y_hat

def one_class_svm(data):
    ee = OneClassSVM(nu=0.01)
    y_hat = ee.fit_predict(data)
    return y_hat

def stl(data):
    stl_decomp = STL(data)
    result = stl_decomp.fit()
    _, _, resid = result.seasonal, result.trend, result.resid
    resid_mu = resid.mean()
    resid_dev = resid.std()
    lower = resid_mu - 3 * resid_dev
    upper = resid_mu + 3 * resid_dev
    return np.vectorize(lambda x: True if ((x < lower) or (x > upper)) else False)(resid)

# https://github.com/nachonavarro/seasonal-esd-anomaly-detection
def esd(data):
    outlier_indecies = sesd.seasonal_esd(data['vol'], periodicity=7, hybrid=True, max_anomalies=3)
    return np.vectorize(lambda x: True if x in outlier_indecies else False)([i for i in range(len(data))])
    
def outlier_detector(data):
    data = data.set_index('id')
    mask_iso = isolation_forest(data)
    mask_lof = local_outlier_factor(data)
    mask_iqr = iqr(data).reset_index(drop=True)
    mask_hampel = hampel(data).reset_index(drop=True)
    mask_z_score = z_score(data).reset_index(drop=True)
    mask_mcd = mcd(data)
    mask_svm = one_class_svm(data)
    data.reset_index(inplace=True)
    mask_iso = np.vectorize(lambda x: True if x == -1 else False)(mask_iso)
    mask_lof = np.vectorize(lambda x: True if x == -1 else False)(mask_lof)
    mask_mcd = np.vectorize(lambda x: True if x == -1 else False)(mask_mcd)
    mask_svm = np.vectorize(lambda x: True if x == -1 else False)(mask_svm)
    data['method1'] = mask_iso
    data['method2'] = mask_lof
    data['method3'] = mask_iqr
    data['method4'] = mask_hampel
    data['method5'] = mask_z_score
    data['method6'] = mask_mcd
    data['method7'] = mask_svm
    data.drop('feature', axis=1, inplace=True)
    return data


def outlier_detector_time_series(data):
    data.rename(columns={'month': 'time', 'interest': 'vol'}, inplace=True)
    res = pd.DataFrame()
    res['time'] = data['time']
    data.time = pd.to_datetime(data['time'], format='%Y-%m')
    data = data.set_index('time')
    data = data.asfreq(pd.infer_freq(data.index))
    mask_stl = stl(data)
    mask_esd = esd(data)
    res['method1'] = mask_stl
    res['method2'] = mask_esd
    return res
    
