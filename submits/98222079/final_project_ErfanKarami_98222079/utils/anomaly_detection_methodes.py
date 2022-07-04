from scipy import stats
import numpy as np
import pandas as pd

def anomaly_detector(data, config):
    if config['time_series']:
        # TODO
        return None
    else:
        id_column=data['id']
        data=data.drop(columns=['id'])
        IQR_outliers=iqr_outlier_detector(data)
        zscore_outliers=zscore_outlier_detector(data)
        columns=['id']
        for i in range(len(zscore_outliers.columns)):
            columns.append(IQR_outliers.columns[i])
            columns.append(zscore_outliers.columns[i])
        result=pd.DataFrame(columns=columns)
        print(columns)
        result['id']=id_column.values
        result[IQR_outliers.columns]=IQR_outliers.values
        result[zscore_outliers.columns]=zscore_outliers.values

    return result


def iqr_outlier_detector(data):
    columns=data.columns
    columns=list(map(lambda x: 'IQR_method_'+x,columns))
    # calculate Q1 and Q3
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)

    # calculate the IQR
    IQR = Q3 - Q1

    # filter the dataset with the IQR
    IQR_outliers = (data < (Q1 - 1.5 * IQR)) |(data > (Q3 + 1.5 * IQR))
    IQR_outliers.columns=columns
    return IQR_outliers

def zscore_outlier_detector(data):
    columns=data.columns
    columns=list(map(lambda x: 'zscore_method_'+x,columns))
    data=(data-data.mean(axis=0))/data.std(axis=0)
    zscore_outliers= data >= 3
    zscore_outliers.columns=columns
    return zscore_outliers