import uvicorn
import pandas as pd
from typing import Dict
from fastapi import FastAPI
from khayyam import JalaliDate

from files.types import *
from files.inter_polation import linear_interpolation

from files.outlier.dbscan import dbscan
from files.outlier.isolation_forest import isolation_forest
from files.outlier.localOutlierFactor import local_Outlier_Factor

from files.imbalancedData.overSampling import o_sampling
from files.imbalancedData.underSampler import u_sampling
from files.imbalancedData.Smote import smote

app = FastAPI()


@app.post('/interpolation1')
async def interpol(data: Dict, config: Config):
    df = pd.DataFrame.from_dict(data)
    df['time'] = pd.to_datetime(df['time'], format=r'%Y/%m/%d')
    if config.type == Calender_Type.shamsi:
        result = linear_interpolation(df, config)
        result['time'] = [JalaliDate(time_.date()).strftime(
            r'%Y/%m/%d') for time_ in result['time']]
    else:
        result = linear_interpolation(df, config)

    result = result.to_dict()
    return {'data': result}


@app.post('/interpolation2')
async def tinterpol(data: Dict, config: ConfigOfTimeSwitch):
    df = pd.DataFrame.from_dict(data)
    df['time'] = pd.to_datetime(df['time'], format=r'%Y/%m/%d')
    result = linear_interpolation(df, config)

    result = result.to_dict()
    return {'data': result}


@app.post('/outlier')
async def detection(data: Dict, config: ConfigOfDetection):
    df = pd.DataFrame.from_dict(data)
    if config.timeseries:
        isf = isolation_forest(df)['outliers']
        lo = local_Outlier_Factor(df)['outliers']

        df['isolation_forest'] = isf
        df['lof'] = lo
    else:
        dbscan_ = dbscan(df)['outliers']
        isf = isolation_forest(df)['outliers']

        df['dbscan'] = dbscan_
        df['isolation_forest'] = isf

    result = df.to_dict()
    return {'data': result, 'config': config}


@app.post('/inbalanced')
async def balanced(data: Dict, config: BalancedConfig):
    result = pd.DataFrame()
    major_class_tag = config.major_class_tag
    minor_class_tag = config.minor_class_tag
    if config.method == BalancedConfig.method.SMOTE:
        result = smote(data, major_class_tag, minor_class_tag)
    elif config.method == BalancedConfig.method.oversampling:
        result = o_sampling(data, major_class_tag, minor_class_tag)
    elif config.method == BalancedConfig.method.undersampling:
        result = u_sampling(data, major_class_tag, minor_class_tag)

    result = result.to_dict()
    return {'data': result}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=9000)