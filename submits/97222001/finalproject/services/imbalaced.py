from imblearn.over_sampling import RandomOverSampler as ros
from imblearn.over_sampling import SMOTE as sm
from imblearn.under_sampling import RandomUnderSampler as rus
import pandas as pd

def balanced_data(data, config):
    if config['method'] == 'oversampling':
        ro = ros()
        X = data.drop(['class'], axis=1)
        y = data['class']
        X1, y1 = ro.fit_resample(X, y)
        data = pd.DataFrame(X1, columns=X.columns)
        data['class'] = pd.Series(y1)
    elif config['method'] == 'undersampling':
        ru = rus()
        y = data['class']
        X = data.drop(['class'], axis=1)
        X1, y1 = ru.fit_resample(X, y)
        data = pd.DataFrame(X1, columns=X.columns)
        data['class'] = pd.Series(y1)
    elif config['method'] == 'SMOTE':
        s = sm()
        y = data['class']
        X = data.drop(['class'], axis=1)
        X1, y1 = s.fit_resample(X, y)
        data = pd.DataFrame(X1, columns=X.columns)
        data['class'] = pd.Series(y1)
    return data
