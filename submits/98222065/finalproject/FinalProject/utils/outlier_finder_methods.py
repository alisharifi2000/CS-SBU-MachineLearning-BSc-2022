import numpy as np
from scipy import stats


def find_outliers_using_quantile(data):
    res = np.logical_or(data > data.quantile(0.75), data < data.quantile(0.25))
    return res

def find_outliers_using_z_score(data):
    res = np.abs(stats.zscore(data.feature))
    res = res.gt(3)
    return res
