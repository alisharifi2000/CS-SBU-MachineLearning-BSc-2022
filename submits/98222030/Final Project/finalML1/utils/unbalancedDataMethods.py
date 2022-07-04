import pandas as pd
import numpy as np
import random
from imblearn.over_sampling import SMOTE,RandomOverSampler
from imblearn.under_sampling import TomekLinks

def smote(data,config):
     #valueOfMinorClass = config['minor_class']
     #valueOfMajorClass= config['major_class']

     data = data.set_index('id')

     x = data.drop(['class'], axis=1)
     y = data['class']

     minVal = data['class'].value_counts().min() -1

     sm = SMOTE(random_state = 2,k_neighbors = minVal)
     x_res, y_res = sm.fit_resample(x, y)

     data.reset_index(inplace=True)

     idTemp = []
     for i in range(len(x_res)):
          idTemp.append(i + 1)

     df = pd.DataFrame(columns=["id", "feature1", "class"])
     df["id"] = idTemp
     df["feature1"] = x_res
     df["class"] = y_res

     return df



def oversampling(data,config):
     oversample = RandomOverSampler(sampling_strategy='minority')

     data = data.set_index('id')

     x = data.drop(['class'], axis=1)
     y = data['class']

     x_over, y_over = oversample.fit_resample(x, y)


     data.reset_index(inplace=True)

     idTemp = []
     for i in range(len(x_over)):
          idTemp.append(i+1)


     df = pd.DataFrame(columns=["id", "feature1","class"])
     df["id"] = idTemp
     df["feature1"] = x_over
     df["class"] = y_over

     return df


def undersampling(data,config):

     data = data.set_index('id')
     x = data.drop(['class'], axis=1)
     y = data['class']

     minVal = data['class'].value_counts().min()

     x_under, y_under = sample_together(minVal, x, y)
     data.reset_index(inplace=True)

     idTemp = []
     for i in range(len(x_under)):
          idTemp.append(i+1)


     df = pd.DataFrame(columns=["id", "feature1","class"])
     df["id"] = idTemp
     df["feature1"] = x_under.values
     print(df["feature1"])
     df["class"] = y_under.values

     return df

def sample_together(n, X, y):
    rows = random.sample(np.arange(0,len(X.index)).tolist(),n)
    return X.iloc[rows,], y.iloc[rows,]



def tomekLinksUndersamplingFunc(data,config):

     undersample = TomekLinks()

     data = data.set_index('id')
     x = data.drop(['class'], axis=1)
     y = data['class']
     xt, yt = undersample.fit_resample(x, y)
     data.reset_index(inplace=True)

     idTemp = []
     for i in range(len(xt)):
          idTemp.append(i + 1)



     df = pd.DataFrame(columns=["id", "feature1", "class"])
     df["id"] = idTemp
     df["feature1"] = xt
     df["class"] = yt

     return df

