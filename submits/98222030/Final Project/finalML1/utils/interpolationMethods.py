
import jdatetime
from khayyam import JalaliDate, JalaliDatetime, TehranTimezone
import jalali_pandas
import pandas as pd
from functools import partial
from datetime import datetime
import gzip

def linear_interpolation(data, config):
       if config['type'] == 'miladi':
            if config['time'] == 'daily':
                data = data.set_index('time')
                data = data.resample('D')
                data = data.interpolate(method=config['interpolation'])
                data.reset_index(inplace=True)


            elif config['time'] == 'monthly':
                data = data.set_index('time')
                data = data.resample('M')
                data = data.interpolate(method=config['interpolation'])
                data.reset_index(inplace=True)


            else:
                 data = None

       elif config['type'] == 'shamsi':
            if config['time'] == 'daily':
                data['time'] = data['time'].apply(lambda x: jdatetime.datetime.strptime(x, '%Y-%m-%d').togregorian())
                data = data.set_index('time')
                #data.index = pd.to_datetime(data.index, unit='s')
                data = data.resample(rule='1D').interpolate(method='linear')
                #data = data.interpolate(method=config['interpolation'])
                data.reset_index(inplace=True)
                data['time'] = data.time.apply(lambda x: jdatetime.GregorianToJalali(x.year, x.month, x.day))
                data['time'] = data.time.apply(lambda x: f'{x.jyear}-{x.jmonth}-{x.jday}')

            elif config['time'] == 'monthly':
                data['time'] = data['time'].apply(lambda x: jdatetime.datetime.strptime(x, '%Y-%m-%d').togregorian())
                data = data.set_index('time')
                data = data.resample('M')
                data = data.interpolate(method=config['interpolation'])
                data.reset_index(inplace=True)
                data['time'] = data.time.apply(lambda x: jdatetime.GregorianToJalali(x.year, x.month, x.day))
                data['time'] = data.time.apply(lambda x: f'{x.jyear}-{x.jmonth}-{x.jday}')




       return data


def linear_interpolation2(data, config):
    if config['time'] == 'daily':
        data = data.set_index('time')
        data = data.resample('D')
        data = data.interpolate(method=config['interpolation'])
        data.reset_index(inplace=True)
    elif config['time'] == 'monthly':
        data = data.set_index('time')
        data = data.resample('M')
        data = data.interpolate(method=config['interpolation'])
        data.reset_index(inplace=True)

    else:
        data = None
    return data


def toShamsi(data):
    #data.time.todate()
    #JalaliDatetime()

    data["time"] = data["time"].jalali.to_jalali()
    #data["time"] = data["time"].jalali.to_gregorian()
    #for col in data.columns:
        #print(data)


    data['time'] = data['time'].astype("string")
    data[['time', 'temp']] = data["time"].str.split(" ", 1, expand=True)
    del data['temp']

    print("DataFrame:")
    print(data)

    # apply the dtype attribute
    result = data.dtypes

    print("Output:")
    print(result)

    return data


