import uvicorn
import pandas as pd
from typing import Dict
from fastapi import FastAPI
from khayyam import JalaliDate
from utils.datatypes import *
from utils.interpolation import linear_interpolation
from utils.outlier import isolation_forest, dbscan, lof
from utils.imbalanced_data import oversampling, undersampling, smote

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Hello World!'}


@app.post('/interpolation/simple')
async def interpol(data: Dict, config: Config):
    df = pd.DataFrame.from_dict(data)
    df['time'] = pd.to_datetime(df['time'], format=r'%Y/%m/%d')
    if config.type == CalenderType.shamsi:
        result = linear_interpolation(df, config)
        result['time'] = [JalaliDate(time_.date()).strftime(
            r'%Y/%m/%d') for time_ in result['time']]
    else:
        result = linear_interpolation(df, config)

    result = result.to_dict()
    return {'data': result}


@app.post('/interpolation/timeswitch')
async def tinterpol(data: Dict, config: ConfigTimeSwitch):
    df = pd.DataFrame.from_dict(data)
    df['time'] = pd.to_datetime(df['time'], format=r'%Y/%m/%d')
    result = linear_interpolation(df, config)

    result = result.to_dict()
    return {'data': result}


@app.post('/detect/outlier')
async def detection(data: Dict, config: ConfigDetection):
    df = pd.DataFrame.from_dict(data)
    if config.timeseries:
        isf = isolation_forest(df)['outliers']
        lo = lof(df)['outliers']

        df['isolation_forest'] = isf
        df['lof'] = lo
    else:
        dbscan_ = dbscan(df)['outliers']
        isf = isolation_forest(df)['outliers']

        df['dbscan'] = dbscan_
        df['isolation_forest'] = isf

    result = df.to_dict()
    return {'data': result, 'config': config}


@app.post('/management/balanced')
async def balanced(data: Dict, config: ConfigBalanced):
    result = pd.DataFrame()
    major_class_tag = config.major_class_tag
    minor_class_tag = config.minor_class_tag
    if config.method == ConfigBalanced.method.SMOTE:
        result = smote(data, major_class_tag, minor_class_tag)
    elif config.method == ConfigBalanced.method.oversampling:
        result = oversampling(data, major_class_tag, minor_class_tag)
    elif config.method == ConfigBalanced.method.undersampling:
        result = undersampling(data, major_class_tag, minor_class_tag)

    result = result.to_dict()
    return {'data': result}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=9000)
