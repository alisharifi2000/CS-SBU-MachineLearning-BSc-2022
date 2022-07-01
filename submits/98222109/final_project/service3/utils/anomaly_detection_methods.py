from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from datetime import *
import pandas as pd


def isolation_forest(data,config):
    if(config['time_series'] == True):
        data.set_index("time")
    elif(config['time_series'] == False):
        data.set_index('id')
    data_double = data.copy()
    clf = IsolationForest(max_samples='auto', contamination=0.01)
    clf.fit(data_double)
    data_double['Anomaly'] = clf.predict(data_double)
    temp=list()
    for item in data_double["Anomaly"]:
        if (item == -1):
            temp.append(True)
        else:
            temp.append(False)
    temp2=pd.Series(temp)
    data_double["Anomaly"] = temp2
    data_double.rename(
       columns={
           'Anomaly':'method1'
        },
        inplace = True
    )
    if (config['time_series'] == True):
        del data_double["vol"]
    elif (config['time_series'] == False):
        del data_double["feature"]
    data.reset_index(inplace=True)
    return data_double

def LOF(data,config):
    if(config['time_series'] == True):
        data.set_index("time")
    elif(config['time_series'] == False):
        data.set_index('id')
    data_double = data.copy()
    clf = LocalOutlierFactor(n_neighbors=3)
    data_double['Anomaly'] = clf.fit_predict(data_double)
    temp = list()
    for item in data_double["Anomaly"]:
        if (item == -1):
            temp.append(True)
        else:
            temp.append(False)
    temp2 = pd.Series(temp)
    data_double["Anomaly"] = temp2
    data_double.rename(
        columns={
            'Anomaly': 'method2'
        },
        inplace=True
    )
    if (config['time_series'] == True):
        del data_double["vol"]
    elif (config['time_series'] == False):
        del data_double["feature"]
    data.reset_index(inplace=True)
    return data_double
