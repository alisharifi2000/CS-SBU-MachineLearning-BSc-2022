from imblearn.over_sampling import SMOTE,RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler


def imbalance_manager(data ,config):
    handler=None
    if config['method']=='under sampling':
        handler=RandomUnderSampler()
    elif config['method']=='over sampling':
        handler=RandomOverSampler()
    elif config['method']=='SMOTE':
        minor_class_tag=config['minor_class']
        amount=len(data[data[config['tag_label']]==minor_class_tag])
        if amount==0:
            return 'n_sample for each class must be grater than 1 in SMOTE method...'
        handler=SMOTE(k_neighbors=min(5,amount-1))
    else:
        return 'invalid resampling method!'
    result=handler.fit_resample(X=data.drop(columns=[config['tag_label']]),y=data['class'])
    result[0]['class']=result[1].values

    result[0].reset_index(inplace=True)

    return result[0]