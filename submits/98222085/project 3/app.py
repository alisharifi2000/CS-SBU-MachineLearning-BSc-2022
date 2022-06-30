# Anita Soroush 98222085

from flask import Flask, request
from utils.common import response_message, read_json_time_series, read_json
from utils.interpolation_methods import linear_interpolation
import pandas as pd
from khayyam import *
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest
import statsmodels.api as sm

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def isup():
    return response_message('API is active')


@app.route('/service1', methods=['GET', 'POST'])
def interpolation1():
    req = request.get_json()
    config = req['config']

    if config['type'] == 'miladi':
        data = read_json_time_series(req['data'], type="miladi")
        result = linear_interpolation(data, config)
        result['time'] = result['time'].dt.strftime('%Y-%m-%d')
        result = result.to_json()

    elif config['type'] == 'shamsi':
        data = read_json_time_series(req['data'], type="shamsi")
        result = linear_interpolation(data, config)
        shamsi_equivalent_date_str_list = []
        vol = result['vol']
        for index in range(0, len(result)):
            shamsi_equivalent_date_str = JalaliDatetime(pd.to_datetime(result.iloc[index]['time'])).strftime('%Y-%m-%d')
            shamsi_equivalent_date_str_list.append(shamsi_equivalent_date_str)
        result.drop(['time', 'vol'], axis=1, inplace=True)
        result['time'] = shamsi_equivalent_date_str_list
        result['vol'] = vol
        result = result.to_json()
    return result


@app.route('/service2', methods=['GET', 'POST'])
def interpolation2():
    req = request.get_json()
    config = req['config']
    data = read_json_time_series(req['data'], type='miladi')

    result = linear_interpolation(data, config)
    shamsi_equivalent_date_str_list = []
    vol = result['vol']
    for index in range(0, len(result)):
        shamsi_equivalent_date_str = JalaliDatetime(pd.to_datetime(result.iloc[index]['time'])).strftime('%Y-%m-%d')
        shamsi_equivalent_date_str_list.append(shamsi_equivalent_date_str)
    result.drop(['time', 'vol'], axis=1, inplace=True)
    result['time'] = shamsi_equivalent_date_str_list
    result['vol'] = vol
    result = result.to_json()
    return result


@app.route('/service3', methods=['GET', 'POST'])
def outlier_detector():
    req = request.get_json()
    config = req['config']

    if config["time_series"] == True:
        data = read_json_time_series(req['data'], type='miladi')
        print(data)
        result = data.drop('feature', axis=1)
        result['time'] = result['time'].dt.strftime('%Y-%m-%d')
        data.reset_index(inplace=True)
        data['time'] = pd.to_datetime(data['time'])
        data = data.set_index('time')

        # method 1 : STL
        s = sm.tsa.seasonal_decompose(data.feature)
        seasonal, trend, resid = s.seasonal, s.trend, s.resid

        cleaned_data = seasonal + trend
        resid_mean = resid.mean()
        resid_std = resid.std()
        lower_bound = resid_mean - 2 * resid_std
        upper_bound = resid_mean + 1 * resid_std
        STL_result = []
        for index in range(0, len(data)):
            if (resid[index] < lower_bound) or (resid[index] > upper_bound):
                STL_result.append(True)
            else:
                STL_result.append(False)
        result['STL'] = STL_result

        # method 2: Isolation Forest
        isolation_forest = IsolationForest(contamination=0.004)
        isolation_forest.fit(data[['feature']])
        IS_anomalies = isolation_forest.predict(data[['feature']])
        IS_result = []
        for index in range(0, len(data)):
            if IS_anomalies[index] == -1:
                IS_result.append(True)
            else:
                IS_result.append(False)
        result['IsolationForest'] = IS_result

    elif config["time_series"] == False:
        data = read_json(req['data'])
        print(data)
        result = data.drop('feature', axis=1)

        # method 1: Isolation Forest:
        isolation_forest = IsolationForest(contamination=0.1)
        IS_anomalies = isolation_forest.fit_predict(data[['feature']])
        IS_result = []
        for index in range(0, len(data)):
            if IS_anomalies[index] == -1:
                IS_result.append(True)
            else:
                IS_result.append(False)
        result['IsolationForest'] = IS_result

        # method 2: Local outlier factor
        lof = LocalOutlierFactor()
        LOF_anomalies = lof.fit_predict(data[['feature']])
        LOF_result = []
        for index in range(0, len(data)):
            if LOF_anomalies[index] == -1:
                LOF_result.append(True)
            else:
                LOF_result.append(False)
        result['LocalOutlierFactor'] = LOF_result

        # method 3: One Class SVM
        one_class_SVM = OneClassSVM(nu=0.01)
        one_class_SVM_anomalies = one_class_SVM.fit_predict(data[['feature']])
        one_class_SVM_result = []
        for index in range(0, len(data)):
            if one_class_SVM_anomalies[index] == -1:
                one_class_SVM_result.append(True)
            else:
                one_class_SVM_result.append(False)
        result['OneClassSVM'] = one_class_SVM_result

        # overall outcome:
        overall_result = []
        for index in range(0, len(data)):
            row_result = (result.iloc[index]['OneClassSVM'] and result.iloc[index]['IsolationForest']) or \
                         (result.iloc[index]['OneClassSVM'] and result.iloc[index]['LocalOutlierFactor']) or \
                         (result.iloc[index]['LocalOutlierFactor'] and result.iloc[index]['IsolationForest'])
            overall_result.append(row_result)

        result['OverallResult'] = overall_result
        print(overall_result)

    result = result.to_json()
    return result


@app.route('/service4', methods=['GET', 'POST'])
def imbalance_data_handler():
    req = request.get_json()
    config = req['config']
    data = read_json(req['data'])
    data = data.set_index('id')

    if config["method"] == "over_sampling":
        over_sampler = RandomOverSampler(sampling_strategy='minority')
        X = data.drop('class', axis=1)
        y = data['class']
        X_new, y_new = over_sampler.fit_resample(X, y)

    elif config["method"] == "under_sampling":
        under_sampler = RandomUnderSampler(sampling_strategy='majority')
        X = data.drop('class', axis=1)
        y = data['class']
        X_new, y_new = under_sampler.fit_resample(X, y)

    elif config["method"] == "SMOTE":
        smote = SMOTE(sampling_strategy='minority')
        X = data.drop('class', axis=1)
        y = data['class']
        X_new, y_new = smote.fit_resample(X, y)

    result = X_new
    result['class'] = y_new
    result.reset_index(inplace=True)
    result.rename(columns={'index': 'id'}, inplace=True)
    result['id'] += 1
    result = result.to_json()
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
