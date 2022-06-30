import khayyam
import pandas as pd
import numpy as np
from utils.common import convert_to_miladi, convert_to_shamsi


def pick_method(data, config):
    if config['interpolation'] == 'linear':
        data = data.interpolate(method=config['interpolation'])
    elif config['interpolation'] == 'polynomial' or config['interpolation'] == 'spline':
        data = data.interpolate(method=config['interpolation'], order=config['order'])
    
    return data

def base_interpolation(data, config, rule):
    data = data.set_index('time')
    data = data.resample(rule)

    data = pick_method(data, config)

    data.reset_index(inplace=True)
    return data

def base_monthly(data, config):
    data = data.set_index('time')
    data = data.resample('M').sum()
    data.replace(0, np.NaN, inplace=True)

    data = pick_method(data, config)
    
    data.reset_index(inplace=True)
    return data

def pick_rule(data, config):
    if config['time'] == 'daily':
        data = base_interpolation(data, config, 'D')
    elif config['time'] == 'monthly':
        data = base_monthly(data, config)
    elif config['time'] == 'hour':
        data = base_interpolation(data, config, 'H')
    elif config['time'] == 'min':
        data = base_interpolation(data, config, 'T')
    elif config['time'] == 'sec':
        data = base_interpolation(data, config, 'S')
    else:
        data = None

    return data

def interpolate(data, config):
    if config['type'] == 'miladi':
        data.time = pd.to_datetime(data.time, unit='ms')
        data = pick_rule(data, config)

    elif config['type'] == 'shamsi':
        data.time = data['time'].apply(convert_to_miladi)
        data.time = pd.to_datetime(data.time, format='%Y-%m-%d')
        
        data = pick_rule(data , config)

        if not data is None:
            data.time = data['time'].apply(convert_to_shamsi, time_type=config['time'])
    
    else:
        data = None

    return data

def convert_and_interpolate(data, config):
    data.time = pd.to_datetime(data.time, unit='ms')
    data = pick_rule(data, config)

    if not data is None:
        data.time = data['time'].apply(convert_to_shamsi, time_type=config['time'])
        if 'skip_holiday' in config and config['skip_holiday']:
            if config['time'] == 'daily':
                weekday = data['time'].map(lambda x: khayyam.JalaliDate(x.split('-')[0],
                                                                        x.split('-')[1],
                                                                        x.split('-')[2]).weekday())
                data.drop(data.loc[(weekday == 5) | (weekday == 6)].index, inplace=True)
                data.reset_index(inplace=True)

    return data

