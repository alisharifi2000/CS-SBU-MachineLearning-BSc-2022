import os
import pandas as pd
from imblearn.under_sampling import RandomUnderSampler

def u_sampling(data, major_class_tag, minor_class_tag):
    ru_sampling = RandomUnderSampler()
    X = data.drop([major_class_tag], axis=1)
    y = data[minor_class_tag]
    X_r, y_r = ru_sampling.fit_resample(X, y)
    data = pd.DataFrame(X_r, columns=X.columns)
    data[major_class_tag] = pd.Series(y_r)
    return data
