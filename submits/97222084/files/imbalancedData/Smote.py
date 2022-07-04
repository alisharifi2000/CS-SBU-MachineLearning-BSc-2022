import os
import pandas as pd
from imblearn.over_sampling import SMOTE

def smote(data, major_class_tag, minor_class_tag):
    smot = SMOTE(data)
    X = data.drop([major_class_tag], axis=1)
    y = data[minor_class_tag]
    X_r, y_r = smot.fit_resample(X, y)
    data = pd.DataFrame(X_r, columns=X.columns)
    data[major_class_tag] = pd.Series(y_r)
    return data