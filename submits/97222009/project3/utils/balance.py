import abc
import pandas as pd


class Balancer(abc.ABC):
    def __init__(self, data):
        self._data = data

    def balance(self):
        X, y = self._balance()
        X['class'] = y
        X['id'] = X.index.to_numpy() + 1

        return pd.DataFrame(X, columns=self._data.columns)

    @abc.abstractmethod
    def _balance(self):
        pass


class BalancerRegistry:
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = BalancerRegistry()
        return cls.instance

    def __init__(self):
        self._mapping = {}

    def register(self, name, balancer: type):
        self._mapping[name] = balancer

    def get(self, name):
        balancer: type = self._mapping.get(name)
        if balancer is None:
            raise NotImplementedError
        return balancer


class SMOTEBalancer(Balancer):
    def _balance(self):
        from imblearn.over_sampling import SMOTE
        data = self._data
        min_num = data['class'].value_counts().values[-1]
        if min_num <= 1:
            data = pd.concat([data, data]).reset_index().drop('index', axis=1)
        oversample = SMOTE(k_neighbors=min(min_num, 6))
        X, y = oversample.fit_resample(data.drop(['class', 'id'], axis=1), data['class'])
        return X, y


BalancerRegistry.get_instance().register('SMOTE', SMOTEBalancer)


class OverSamplingBalancer(Balancer):
    def _balance(self):
        from imblearn.over_sampling import RandomOverSampler
        data = self._data
        ros = RandomOverSampler(random_state=1)
        X, y = ros.fit_resample(data.drop(['class', 'id'], axis=1), data['class'])
        return X, y


BalancerRegistry.get_instance().register('Oversampling', OverSamplingBalancer)


class TomekLinksBalancer(Balancer):
    def _balance(self):
        from imblearn.under_sampling import TomekLinks
        data = self._data
        tl = TomekLinks(sampling_strategy='auto')
        X, y = tl.fit_resample(data.drop(['class', 'id'], axis=1), data['class'])
        return X, y


BalancerRegistry.get_instance().register('Tomeklinks', TomekLinksBalancer)



class UnderSamplingBalancer(Balancer):
    def _balance(self):
        from imblearn.under_sampling import RandomUnderSampler
        data = self._data
        rus = RandomUnderSampler(random_state=1)
        X, y = rus.fit_resample(data.drop(['class', 'id'], axis=1), data['class'])
        return X, y


BalancerRegistry.get_instance().register('UnderSampling', UnderSamplingBalancer)
