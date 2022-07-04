def interpolation(data, config):
    data = data.set_index('time')

    if config['time'] == 'minutely':
        data = data.resample('1min')
    elif config['time'] == 'hourly':
        data = data.resample('1T')
    elif config['time'] == 'daily':
        data = data.resample('D')
    elif config['time'] == 'monthly':
        data = data.resample('M')
    else:
        raise ValueError('Invalid time value')
    
    if config['interpolation'] == 'linear':
        data = data.interpolate(method=config['interpolation'])
    elif config['interpolation'] == 'spline':
        data = data.interpolate(method=config['interpolation'], order=config['order'])
    elif config['interpolation'] == 'polynomial':
        data = data.interpolate(method=config['interpolation'], order=config['order'])
    else:
        raise ValueError('Invalid interpolation value')

    data.reset_index(inplace=True)


    return data
