import datetime

from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import SMOTE
from khayyam import JalaliDatetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from sklearn.covariance import EllipticEnvelope
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM

from core.serializers import InterpolationSerializer, OutlierDetectionSerializer, UnbalancedManagingSerializer

import pandas as pd
import numpy as np


class InterpolationView(GenericViewSet):
    serializer_class = InterpolationSerializer
    drift_map = {
        '1M': datetime.timedelta(days=30),
        '1w': datetime.timedelta(weeks=1),
        '1d': datetime.timedelta(days=1),
        '1h': datetime.timedelta(hours=1),
        '1m': datetime.timedelta(minutes=1),
    }

    def post(self, request, *args, **kwargs):
        serializer: InterpolationSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data

        was_shamsi = self.convert_to_miladi(validated_data)

        df = pd.DataFrame(validated_data['data'])
        df['time'] = pd.to_datetime(df.time)
        df.sort_values('time', inplace=True)
        d1 = df.time.iloc[0]
        dn = df.time.iloc[-1]
        df.set_index('time', inplace=True)
        while d1 < dn:
            d1 = d1 + self.drift_map.get(validated_data['time'])
            if validated_data['skip_holiday'] and d1.day_of_week in [4, 5]:
                # Ignore friday and saturday
                continue
            if d1 not in df.index:
                df.loc[d1] = [np.NaN for _ in range(1)]

        df.sort_values('time', inplace=True)
        df = df.astype(np.float64)

        df.interpolate(method=validated_data['interpolation'], inplace=True)

        if was_shamsi:
            self.convert_to_jalali(df)

        return Response(data=df.to_html(), status=status.HTTP_200_OK)

    def convert_to_miladi(self, validated_data):
        is_shamsi = validated_data['type'] == 'shamsi'
        if is_shamsi:
            for i in range(len(validated_data['data'])):
                date = validated_data['data'][i]['time']
                try:
                    jalali_date = JalaliDatetime.strptime(date, '%Y/%m/%d %H:%M:%S').todatetime()
                except Exception:
                    jalali_date = JalaliDatetime.strptime(date, '%Y/%m/%d').todatetime()
                validated_data['data'][i]['time'] = jalali_date
        return is_shamsi

    def convert_to_jalali(self, df: pd.DataFrame):
        df.reset_index(inplace=True)
        for i, row in df.iterrows():
            jalali = JalaliDatetime(row.time)
            date_str = jalali.strftime('%Y/%m/%d %H:%M:%s')
            df.loc[i, 'time'] = date_str


class OutlierDetectionView(GenericViewSet):
    serializer_class = OutlierDetectionSerializer

    def post(self, request, *args, **kwargs):
        serializer: OutlierDetectionSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data

        if validated_data['time_series']:
            df = self.time_series_detection(validated_data['data'])
        else:
            df = self.normal_outlier_detection(validated_data['data'])

        return Response(data=df.to_html(), status=status.HTTP_200_OK)

    def time_series_detection(self, data) -> pd.DataFrame:
        df = pd.DataFrame(data)
        cols = set(df.columns) - {'time'}
        self.derivative(df, cols)
        self.isolation_forest_detector(df, cols)
        self.local_outlier_factor(df, cols)
        self.one_class_svm(df, cols)
        return df

    def normal_outlier_detection(self, data) -> pd.DataFrame:
        df = pd.DataFrame(data)
        cols = set(df.columns) - {'time'}
        self.isolation_forest_detector(df, cols)
        self.local_outlier_factor(df, cols)
        self.one_class_svm(df, cols)
        self.minimum_covariance_determinant(df, cols)
        return df

    @classmethod
    def isolation_forest_detector(cls, df, cols):
        iso = IsolationForest(n_jobs=-1)
        y = iso.fit_predict(df[list(cols)])
        col = []
        for i in y:
            if i == -1:
                col.append(True)
            else:
                col.append(False)
        df['isolation_forest'] = col

    @classmethod
    def local_outlier_factor(cls, df, cols):
        lof = LocalOutlierFactor(n_jobs=-1, n_neighbors=2, leaf_size=2)
        y = lof.fit_predict(df[list(cols)])
        col = []
        for i in y:
            if i == -1:
                col.append(True)
            else:
                col.append(False)
        df['local_outlier_factor(KNN)'] = col

    @classmethod
    def one_class_svm(cls, df, cols):
        ocs = OneClassSVM()
        y = ocs.fit_predict(df[list(cols)])
        col = []
        for i in y:
            if i == -1:
                col.append(True)
            else:
                col.append(False)
        df['one_class_svm'] = col

    @classmethod
    def minimum_covariance_determinant(cls, df, cols):
        ee = EllipticEnvelope()
        y = ee.fit_predict(df[list(cols)])
        col = []
        for i in y:
            if i == -1:
                col.append(True)
            else:
                col.append(False)
        df['minimum_covariance_determinant'] = col

    def derivative(self, df, cols):
        df['derivative'] = [False for i in range(df.shape[0])]
        for column in cols:
            self.check_for_col(column, df)

    @classmethod
    def check_for_col(cls, column, df):
        help_df = df.copy()
        new_col_name = f'{column}-diff'
        help_df[new_col_name] = help_df[column].diff().abs()
        help_df[new_col_name] /= help_df[new_col_name].max()
        for index, row in help_df.iterrows():
            if index == 0:
                continue
            if row[new_col_name] > 0.48 and not df.at[index - 1, 'derivative']:
                df.at[index, 'derivative'] = True


class UnbalancedManagingView(GenericViewSet):
    serializer_class = UnbalancedManagingSerializer

    def post(self, request, *args, **kwargs):
        serializer: UnbalancedManagingSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.data

        if validated_data['method'] == 'oversampling':
            df = self.over_sample(validated_data)
        elif validated_data['method'] == 'undersampling':
            df = self.under_sample(validated_data)
        else:
            df = self.smothe(validated_data)

        return Response(data=df.to_html(), status=status.HTTP_200_OK)

    @classmethod
    def over_sample(cls, validated_data) -> pd.DataFrame:
        df = pd.DataFrame(validated_data['data'])
        ros = RandomOverSampler(random_state=42)
        x, y = ros.fit_resample(df.drop('target', axis=1, inplace=False), df.target)
        x['target'] = y
        return x

    @classmethod
    def under_sample(cls, validated_data) -> pd.DataFrame:
        df = pd.DataFrame(validated_data['data'])
        rus = RandomUnderSampler(random_state=42)
        x, y = rus.fit_resample(df.drop('target', axis=1, inplace=False), df.target)
        x['target'] = y
        return x

    @classmethod
    def smothe(cls, validated_data) -> pd.DataFrame:
        df = pd.DataFrame(validated_data['data'])
        smothe = SMOTE(random_state=42, k_neighbors=2)
        x, y = smothe.fit_resample(df.drop('target', axis=1, inplace=False), df.target)
        x['target'] = y
        return x
