def linear_interpolation(data, config):
    import khayyam as kh
    import pandas as pd
    if config.type == 'shamsi':
        dates = []
        for d in data.time:
            temp = kh.JalaliDatetime(*list(d.split('-'))).todatetime()
            temp = pd.to_datetime(temp)
            dates.append(temp)
        data.time = dates
    else:
        data.time = pd.to_datetime(data.time, infer_datetime_format=True)

    dic_str = {'monthly': '%Y-%m', 'daily': '%Y-%m-%d'}
    dic_offset = {'monthly': 'pd.offsets.MonthBegin(1)',
                  'daily': 'pd.offsets.Day(1)'}

    data.time = pd.to_datetime(data.time.dt.strftime(dic_str[config.time]), infer_datetime_format=True)
    s = data.time[0]
    f = data.time[-1]
    index = pd.date_range(start=s, end=f, freq=eval(dic_offset[config.time]))

    data.index = data.time
    index_list = data.index.to_list()
    for i in index:
        if i not in index_list:
            data.loc[i] = None

    data = data.sort_index()

    out = data.drop('time', axis=1)

    if config.interpolation == 'linear':
        out.vol = out.vol.interpolate()
    elif config.interpolation == 'poly':
        out.vol = out.vol.interpolate(method='polynomial', order=int(config.interpolation[4:]))
    elif config.interpolation == 'pad':
        out.vol = out.vol.interpolate(method='pad')


    out = out.reset_index().to_json()
    out = {'data': out}
    return out
