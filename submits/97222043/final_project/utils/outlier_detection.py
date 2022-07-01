from adtk.detector import SeasonalAD
from adtk.detector import ThresholdAD
from adtk.detector import PersistAD
import numpy as np
import pandas as pd
from scipy import stats
def anomoly_detection(data, config):
    if config["method"] == "seasonal":
        seasonal_vol = SeasonalAD(freq = config["freq"])
        anomalies = seasonal_vol.fit_detect(data)
        anomalies.reset_index(inplace=True)
        return anomalies
    elif config["method"] == "threshold":
        threshold_vol = ThresholdAD(low = config["low"], high = config["high"])
        anomalies = threshold_vol.detect(data)
        anomalies.reset_index(inplace=True)
        return anomalies
    elif config["method"] == "persist":
        persist_vol = PersistAD()
        anomalies = persist_vol.fit_detect(data)
        anomalies.reset_index(inplace=True)
        return anomalies

def outlier_detection(data,config):
    if config["method"] == "zscore":
        z = np.abs(stats.zscore(data[config["feature"]]))
        print(z)
        final_array = []
        boolarr = (z > 3)
        print(boolarr)
        result = np.where(boolarr)
        print(result)
        id_arr = []
        feature_array = []
        for x in range(len(boolarr)):
            id_arr.append(x)
            feature_array.append(boolarr[x])
        final_df = pd.DataFrame({"id": id_arr, config["feature"]:feature_array})
        return final_df
    elif config["method"] =="IQR":
        Q1 = np.percentile(data[config["feature"]], 25,
                   interpolation = 'midpoint')
 
        Q3 = np.percentile(data[config["feature"]], 75,
                        interpolation = 'midpoint')
        IQR = Q3 - Q1
        final_array = []
        upper = Q3+1.5*IQR
        lower = Q1 - 1.5 * IQR
        id_list = list(range(len(data)))
        for x in data[config["feature"]]:
            if x <= lower or x >= upper:
                final_array.append(True)
            else:
                final_array.append(False)
        final_df = pd.DataFrame({"id":id_list,config["feature"]:final_array})
        return final_df
