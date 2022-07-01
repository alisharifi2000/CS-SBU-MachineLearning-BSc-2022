from sklearn.utils import resample
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import NearMiss
import pandas as pd

def undersampling(df,minor_class,major_class):
    df_major = df[df['class'] == major_class ]
    df_minor = df[df['class'] == minor_class ]
    n_minor = len(df_minor)
    df_under_sampled = resample(df_major,n_samples =n_minor, random_state=42)
    return pd.concat([df_minor,df_under_sampled])

def oversampling(df,minor_class,major_class):
    df_major = df[df['class'] == major_class ]
    df_minor = df[df['class'] == minor_class ]
    n_major = len(df_major)
    df_over_sampled = resample(df_minor,n_samples =n_major, random_state=42)
    return pd.concat([df_major,df_over_sampled])

def smote_method(df,minor_class,major_class):
    df_minor = df[df['class'] == minor_class]
    n_minor = len(df_minor)
    smote = SMOTE(sampling_strategy='minority',k_neighbors=min(5,n_minor-1),random_state=42)
    oversampled_X , oversampled_y = smote.fit_resample(df.drop('class',axis=1),df['class'])
    return pd.concat([oversampled_X , oversampled_y],axis=1)


def Near_Miss(df,minor_class):
    df_minor = df[df['class'] == minor_class]
    n_minor = len(df_minor)
    nearMiss = NearMiss(n_neighbors=min(3,n_minor))
    undersampled_X , undersampled_y = nearMiss.fit_resample(df.drop('class',axis=1),df['class'])
    return pd.concat([undersampled_X , undersampled_y],axis=1)
