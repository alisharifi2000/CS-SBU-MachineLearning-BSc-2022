#import pandas
import pandas as pd
# load dataset
train_data = pd.read_csv("train.csv")
test_data = pd.read_csv("test.csv")
#split dataset in features and target variable
cols = list(train_data.columns)
columns = cols.copy()
print(cols)
from sklearn import preprocessing
def encode_features(df_train, df_test,features):
    df_combined = pd.concat([df_train[features], df_test[features]])
    
    for feature in features:
        le = preprocessing.LabelEncoder()
        le = le.fit(df_combined[feature])
        df_train[feature] = le.transform(df_train[feature])
        df_test[feature] = le.transform(df_test[feature])
    return df_train, df_test
# import the class
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.20,random_state=23)
# instantiate the model (using the default parameters)
logreg = LogisticRegression()
best_features = []
all_features = columns.copy()
################################
#coded by me 
def forward_selection():
    while len(best_features) < 5:
        max_auc = 0
        auc_feature = ""
        for this_feature in all_features:
            features = best_features.append(this_feature)
            train_df, test_df = encode_features(train_data, test_data,features)
            X_all = train_df[features]
            y_all = train_data["price_range"]
            X_train,X_test,y_train,y_test=train_test_split(X_all,y_all,test_size=0.20,random_state=23)
            logreg.fit(X_train,y_train)
            y_pred_proba = logreg.predict_proba(X_test)[::,1]
            auc = metrics.roc_auc_score(y_test, y_pred_proba)
            if auc > max_auc:
                max_auc = auc
                auc_feature = this_feature
        best_features.append(auc_feature)
        all_features.remove(auc_feature)
###################################
#end of my code
# fit the model with data
logreg.fit(X_train,y_train)
print("after fit")
#
y_pred=logreg.predict(X_test)
# import the metrics class
# import required modules
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
y_pred_proba = logreg.predict_proba(X_test)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba)
auc = metrics.roc_auc_score(y_test, y_pred_proba)