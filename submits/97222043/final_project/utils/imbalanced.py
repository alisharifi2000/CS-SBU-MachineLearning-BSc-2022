import pandas as pd
from imblearn.over_sampling import RandomOverSampler,SMOTE, ADASYN
from imblearn.under_sampling import RandomUnderSampler,ClusterCentroids,NearMiss
from sklearn.cluster import k_means
def balance_imbalanced(X:pd.DataFrame,y:pd.DataFrame, config):
    method = config["method"]
    if method == "RandomOverSample":
        ros = RandomOverSampler(random_state=0)
        X_resampled,y_resampled = ros.fit_resample(X,y)
    elif method == "SMOTE":
        X_resampled, y_resampled = SMOTE().fit_resample(X, y)
    elif method == "ADASYN":
        X_resampled, y_resampled = ADASYN().fit_resample(X, y)
    elif method == "RandomUnderSample":
        X_resampled, y_resampled = RandomUnderSampler(random_state=0).fit_resample(X, y)
    elif method == "ClusterCentroids":
        X_resampled, y_resampled = ClusterCentroids(random_state=0).fit_resample(X, y)
    elif method == "NearMiss":
        X_resampled, y_resampled = NearMiss(version=1).fit_resample(X, y)
    else:
        raise ValueError("Chose from methods")
    return pd.concat([X_resampled,y_resampled], axis="columns")