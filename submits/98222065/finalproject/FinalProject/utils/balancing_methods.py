from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler


def balancing(data ,config):

    result = []
    X = data.drop(['class'], axis=1)
    y = data['class']
    if config['method'] == "SMOTE":
        major = config['major_class']
        minor = config['minor_class']
        count = data['class'].value_counts()[major]
        smotesampler = SMOTE(k_neighbors=1 , sampling_strategy = {minor : count} )
        X_smote, y_smote = smotesampler.fit_resample(X, y)
        result = X_smote.join(y_smote)

    elif config['method'] == "oversampling":
        oversample = RandomOverSampler(sampling_strategy=0.6)
        X_over, y_over = oversample.fit_resample(X, y)
        result = X_over.join(y_over)

    elif config['method'] == "undersampling":
        undersample = RandomUnderSampler(sampling_strategy=0.5)
        X_under, y_under = undersample.fit_resample(X, y)
        result = X_under.join(y_under)
    return result
