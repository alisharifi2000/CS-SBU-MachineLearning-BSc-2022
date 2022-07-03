def date_conversion(data, config):
    import khayyam as kh
    import pandas as pd
    from datetime import date, datetime
    if config['type'] == 'shamsi':
        dates = []
        for d in data['time']:
            tmp = kh.JalaliDatetime(*list(d.split('-'))).todatetime()
            tmp = pd.to_datetime(tmp)
            dates.append(tmp)
        data['time'] = dates
    else:
        data['time'] = pd.to_datetime(data['time'], infer_datetime_format=True)

    dic_str = {'monthly': '%Y-%m', 'daily': '%Y-%m-%d'}
    dic_offset = {'monthly': 'pd.offsets.MonthBegin(1)',
                  'daily': 'pd.offsets.Day(1)'}

    data['time'] = pd.to_datetime(data['time'].dt.strftime(dic_str[config['time']]), infer_datetime_format=True)
    s = data['time'][0]
    f = data['time'][-1]
    index = pd.date_range(start=s, end=f, freq=eval(dic_offset[config['time']]))

    data.index = data['time']
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
    elif config.interpolation == 'spline':
        out.vol = out.vol.interpolate(method='spline')

    data.time = data.index

    date_str = []
    for i in range(len(data)):
        dt_obj = datetime.strptime(str(data['time'].iloc[i]), '%Y-%m-%d %H:%M:%S')
        date_str.append(str(dt_obj).split(' ')[0])

    for i in range(len(date_str)):
        temp = date_str[i].split('-')
        year = int(temp[0])
        month = int(temp[1])
        day = int(temp[2])
        date_str[i] = str(kh.JalaliDate(date(year, month, day)))

    data['time'] = date_str

    data.set_index('time', inplace=True)
    out = data.reset_index().to_json()
    out = {'data': out}

    return out

