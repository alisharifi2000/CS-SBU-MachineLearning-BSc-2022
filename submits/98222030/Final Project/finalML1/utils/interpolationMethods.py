from khayyam import JalaliDate, JalaliDatetime, TehranTimezone
import jalali_pandas
import pandas as pd
from functools import partial
from datetime import datetime
import gzip

def linear_interpolation(data, config):
       # if config['type'] == 'miladi':
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
      #  elif config['type'] == 'shamsi':

     #       if config['time'] == 'daily':
       #         data = data.set_index('time')
       #         data = data.resample('D')
       #         data = data.interpolate(method=config['interpolation'])
        #        data.reset_index(inplace=True)
        #    elif config['time'] == 'monthly':
        #        data = data.set_index('time')
          #      data = data.resample('M')
          #      data = data.interpolate(method=config['interpolation'])
         #       data.reset_index(inplace=True)


        #    else:
        #        data = None




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


def convertShamsiMiladi(shamsiDateTime):
    shamsiDateTime = shamsiDateTime.split(sep='-')
    shamsiDateTime = JalaliDatetime(int(shamsiDateTime[0]), int(shamsiDateTime[1]), int(shamsiDateTime[2]),
                                    int(shamsiDateTime[3])
                                    , int(shamsiDateTime[4]), int(shamsiDateTime[5]), int(shamsiDateTime[6]))
    return shamsiDateTime.todatetime()
