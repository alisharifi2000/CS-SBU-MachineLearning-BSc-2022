import pandas as pd
from imblearn.over_sampling import RandomOverSampler, SMOTE
from imblearn.under_sampling import RandomUnderSampler


def smote(df):  # each class must have at least two element
    seed = 100
    k = 1
    X = df.loc[:, df.columns != 'class']
    y = df['class']
    sm = SMOTE(sampling_strategy='auto', k_neighbors=k, random_state=seed)
    X_res, y_res = sm.fit_resample(X, y)
    result = pd.concat([pd.DataFrame(X_res), pd.DataFrame(y_res)], axis=1)
    return result


def random_oversampling(df):  # oversampling that minor class have as many elements as major class
    X = df.loc[:, df.columns != 'class']
    y = df['class']
    oversample = RandomOverSampler(sampling_strategy='minority')
    X_over, y_over = oversample.fit_resample(X, y)
    result = pd.concat([pd.DataFrame(X_over), pd.DataFrame(y_over)], axis=1)
    return result

def random_undersampling(df):
    X = df.loc[:, df.columns != 'class']
    y = df['class']
    undersample = RandomUnderSampler(sampling_strategy='majority')
    X_over, y_over = undersample.fit_resample(X, y)
    result = pd.concat([pd.DataFrame(X_over), pd.DataFrame(y_over)], axis=1)
    return result