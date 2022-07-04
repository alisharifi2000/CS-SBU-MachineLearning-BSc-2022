import os
import pandas as pd
from imblearn.over_sampling import RandomOverSampler

def o_sampling(data, major_class_tag, minor_class_tag):
    ro_sampling = RandomOverSampler()
    X = data.drop([major_class_tag], axis=1)
    y = data[minor_class_tag]
    X_r, y_r = ro_sampling.fit_resample(X, y)
    data = pd.DataFrame(X_r, columns=X.columns)
    data[major_class_tag] = pd.Series(y_r)
    return data