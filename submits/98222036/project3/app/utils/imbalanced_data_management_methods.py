from imblearn.over_sampling import RandomOverSampler, SMOTE
from imblearn.under_sampling import RandomUnderSampler
import pandas as pd

def balanced_data(data, config):
    try:
        if config['method'] == 'oversampling':
            ros = RandomOverSampler()
            X = data.drop(['class'], axis=1)
            y = data['class']
            X_r, y_r = ros.fit_resample(X, y)
            data = pd.DataFrame(X_r, columns=X.columns)
            data['class'] = pd.Series(y_r)
        elif config['method'] == 'undersampling':
            rus = RandomUnderSampler()
            X = data.drop(['class'], axis=1)
            y = data['class']
            X_r, y_r = rus.fit_resample(X, y)
            data = pd.DataFrame(X_r, columns=X.columns)
            data['class'] = pd.Series(y_r)
        elif config['method'] == 'SMOTE':
            sm = SMOTE()
            X = data.drop(['class'], axis=1)
            y = data['class']
            X_r, y_r = sm.fit_resample(X, y)
            data = pd.DataFrame(X_r, columns=X.columns)
            data['class'] = pd.Series(y_r)

    except Exception as e:
        raise e

    return data

"""

"""
