import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN

def zscore(data,config):
    upperBound = data['feature'].mean() + 3*data['feature'].std()
    lowerBound = data['feature'].mean() - 3 * data['feature'].std()

    print(upperBound)
    print(lowerBound)

    data["method1"] = ""
    for i in range(len(data.feature)) :

        if((upperBound < data.feature.iat[i]) or (lowerBound > data.feature.iat[i])):
            data["method1"].iat[i] = False
        else:
            data["method1"].iat[i] = True


    return data

def IQR(data,config):
    Q1, Q3 = np.percentile(data['feature'], [25, 75])
    IQR = Q3 - Q1
    ul = Q3 + 1.5 * IQR
    ll = Q1 - 1.5 * IQR

    data["method2"] = ""
    for i in range(len(data.feature)):

        if ((ul < data.feature.iat[i]) or (ll > data.feature.iat[i])):

            data["method2"].iat[i] = False
        else:
            data["method2"].iat[i] = True

    return data


def isolationForest(data):

    clf = IsolationForest(random_state=0)
    clf.fit(data["feature"].values.reshape(-1, 1))
    pred = clf.predict(data["feature"].values.reshape(-1, 1))
    data["method3"] = ""
    data["method3"] = (pred != 1)
    return data



def isolationForestTime(data):
    clf = IsolationForest(n_estimators = 10, contamination= 'auto', n_jobs=-1)
    clf.fit(data["feature"].values.reshape(-1, 1))
    pred = clf.predict(data["feature"].values.reshape(-1, 1))
    data["method1"] = ""
    data["method1"] = (pred != 1)
    return data

def dbscan(data):
    clusters = DBSCAN(eps=0.8, metric='manhattan', min_samples=3 ,n_jobs=-1).fit(data["feature"].values.reshape(-1, 1))
    labels = clusters.labels_
    data["method2"] = ""
    data["method2"] = (labels == -1)
    return data










