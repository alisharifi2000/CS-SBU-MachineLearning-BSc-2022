import pandas as pd
from sklearn.cluster import DBSCAN as scan
def dbscan(df):
    model = scan(eps = 0.4, min_samples = 10).fit(df)
    outliers = df[model.labels_ == -1]
    df['outliers'] = outliers
    return df

