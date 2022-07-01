import pandas as pd
from sklearn.ensemble import IsolationForest as i_f

def isolation_forest(df):
    df['time'] = pd.to_datetime(df['time'], format=r'%Y/%m/%d')
    df.reset_index(inplace=True)
    model = i_f(contamination=0.1, max_samples='auto')
    model.fit(df[['vol']])
    df['outliers'] = pd.Series(model.predict(df[['vol']])).apply(
        lambda x: 'yes' if (x == -1) else 'no')
    df = df[df['outliers'] == 'yes']
    return df
