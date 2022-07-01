def interpolation(data, config):
    data = data.set_index('time')
    if config['time'] == 'daily':
        data = data.resample('D')
    elif config['time'] == 'monthly':
        data = data.resample('M')
    elif config['time'] == 'hourly':
        data = data.resample('60Min')
    elif config['time'] == 'minutely':
        data = data.resample('1Min')
    else:
        data = None
    if config["interpolation"] == "spline" or config["interpolation"] =="polynomial" :
       data = data.interpolate(method=config['interpolation'],order = config["order"])
    else: 
        data = data.interpolate(method=config['interpolation'])
    if "time_series" not in config.keys():
        data.reset_index(inplace=True)
    return data
