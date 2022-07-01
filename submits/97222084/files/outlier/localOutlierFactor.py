import pandas as pd
from sklearn.neighbors import LocalOutlierFactor as llf

def local_Outlier_Factor(df):
    clf = llf(n_neighbors=10)
    df['outliers'] = clf.fit_predict(df)
    return df