from imblearn.under_sampling import NearMiss, RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler, SMOTE, BorderlineSMOTE, SVMSMOTE, ADASYN


def base_sampler(data, sampler):
    y = data['class']
    X = data.drop('class', axis=1)
    X, y = sampler.fit_resample(X, y)
    X['class'] = y
    X.drop('id', inplace=True, axis=1)
    X.reset_index(inplace=True, drop=False)
    X.rename(columns={'index': 'id'}, inplace=True)
    return X

def oversampler(data):
    os = RandomOverSampler(0.5)
    res = base_sampler(data, os)
    return res

def near_miss(data):
    ns = NearMiss(0.5, n_neighbors=1)
    res = base_sampler(data, ns)
    return res

def smote(data):
    sm = SMOTE(k_neighbors=1)
    res = base_sampler(data, sm)
    return res

def undersampler(data):
    us = RandomUnderSampler(0.5)
    res = base_sampler(data, us)
    return res

def borderline_smote(data):
    sm = BorderlineSMOTE(k_neighbors=1)
    res = base_sampler(data, sm)
    return res

def svm_smote(data):
    sm = SVMSMOTE(k_neighbors=1)
    res = base_sampler(data, sm)
    return res

def adasyn(data):
    asn = ADASYN(n_neighbors=2)
    res = base_sampler(data, asn)
    return res

