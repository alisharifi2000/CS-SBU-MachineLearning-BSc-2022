from os import major, minor
from imblearn.over_sampling import RandomOverSampler, SMOTE
from imblearn.under_sampling import RandomUnderSampler
import pandas as pd



def oversampling(data, major_class_tag, minor_class_tag):
    ros = RandomOverSampler()
    X = data.drop([major_class_tag], axis=1)
    y = data[minor_class_tag]
    X_r, y_r = ros.fit_resample(X, y)
    data = pd.DataFrame(X_r, columns=X.columns)
    data[major_class_tag] = pd.Series(y_r)
    return data

def undersampling(data, major_class_tag, minor_class_tag):
    rus = RandomUnderSampler()
    X = data.drop([major_class_tag], axis=1)
    y = data[minor_class_tag]
    X_r, y_r = rus.fit_resample(X, y)
    data = pd.DataFrame(X_r, columns=X.columns)
    data[major_class_tag] = pd.Series(y_r)
    return data


def smote(data, major_class_tag, minor_class_tag):
    sm = SMOTE(data)
    X = data.drop([major_class_tag], axis=1)
    y = data[minor_class_tag]
    X_r, y_r = sm.fit_resample(X, y)
    data = pd.DataFrame(X_r, columns=X.columns)
    data[major_class_tag] = pd.Series(y_r)
    return data
