class OutlierDetector:

    def __init__(self, data, config):
        self._data = data
        self._config = config
        self._feature = None

    def run(self):
        self._preprocess()
        self._detect()
        return self._data

    def _preprocess(self):
        if self._config.time_series:
            data = self._data.set_index(self._data.time).drop('time', axis=1)
        else:
            data = self._data.set_index(self._data.id).drop('id', axis=1)

        feature = data.feature.copy()
        self._feature = feature
        self._data = data

    def _detect(self):
        data = self._data
        feature = self._feature
        config = self._config
        from statsmodels.tsa.ar_model import AutoReg

        df = data.copy()
        Q1 = df.quantile(0.3)
        Q3 = df.quantile(0.7)
        IQR = Q3 - Q1
        indices = df[((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)].index
        indices = indices.to_list()
        outliers1 = ['true' if data.index[i] in indices else 'false' for i in range(len(data))]



        import numpy as np
        from sklearn.cluster import DBSCAN
        def Scaler(data):
            values = data.feature.copy()
            min_val = abs(values.min())
            values += min_val
            values /= values.max()
            return values

        feature = Scaler(data)
        X = feature.to_numpy().reshape((len(feature), 1))

        clustering = DBSCAN(eps=0.1, min_samples=len(feature) // 20 + 2).fit(X)

        outliers2 = list(map(lambda x: 'true' if x == -1 else 'false',
                             clustering.labels_))

        if config.time_series:
            data['method1'] = outliers1
            data['method2'] = outliers2
        else:
            data['method1'] = outliers1
            data['method2'] = outliers2

        self._data = data
