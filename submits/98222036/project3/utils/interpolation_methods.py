time_freq_type = {'seconds':'S', 'minutes':'T', 'hours':'H', 'daily':'D', 'monthly':'M', 'yearly':'Y'}

def interpolate(data, config):
    try:
        data = data.set_index('time')
        if ('frequency' in config):
            data = data.resample(str(config['frequency']) + time_freq_type[config['time']])
        else:
            data = data.resample(time_freq_type[config['time']])
        
        if ('interpolation_order' in config):
            data = data.interpolate(method=config['interpolation'], order=config['interpolation_order'])
        else:
            data = data.interpolate(method=config['interpolation'], order=1)
        data.reset_index(inplace=True)

        if ('skip_holiday' in config and config['skip_holiday']):
            tem_time = data.time
            tem_day = tem_time.map(lambda t: t.weekday())
            data = data.set_index('time')
            data.drop(tem_time.loc[(tem_day == 3) | (tem_day == 4)].values, inplace=True)
            data.reset_index(inplace=True)

    except Exception as e:
        raise e

    return data
