import pandas as pd
from sklearn.ensemble import IsolationForest
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.neighbors import LocalOutlierFactor



def isolation_forest(df):
    df['time'] = pd.to_datetime(df['time'], format=r'%Y/%m/%d')
    df.reset_index(inplace=True)
    model = IsolationForest(contamination=0.1, max_samples='auto')
    model.fit(df[['vol']])
    df['outliers'] = pd.Series(model.predict(df[['vol']])).apply(
        lambda x: 'yes' if (x == -1) else 'no')
    df = df[df['outliers'] == 'yes']
    return df


def dbscan(df):
    model = DBSCAN(eps = 0.4, min_samples = 10).fit(df)
    outliers = df[model.labels_ == -1]
    df['outliers'] = outliers
    return df


def lof(df):
    clf = LocalOutlierFactor(n_neighbors=10)
    df['outliers'] = clf.fit_predict(df)
    return df
