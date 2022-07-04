import khayyam
import pandas as pd

def time_series_interpolation(data, config):

    if config['time'] == 'daily':
        data = data.set_index('time')
        data = data.resample('D')
        data = data.interpolate(method=config['interpolation'],order =config['order'])
        data.reset_index(inplace=True)

    elif config['time'] == 'monthly':
        data = data.set_index('time')
        data = data.resample('M')
        data = data.interpolate(method=config['interpolation'],order =config['order'])
        data.reset_index(inplace=True)

    else:
        data = None

    return data


def date_converter(date):
  year,month,day = (map(int,date.split('-')))
  return khayyam.JalaliDate(year,month,day).todate()



def jalali_interpolation(data, config):
    # converting to miladi
    data['time']=data.time.apply(date_converter)
    data.time = pd.to_datetime(data.time)

    data = time_series_interpolation(data,config)

    # convert back to shamsi
    data['time']= data.time.apply(convert_to_jalali)
    return data


def convert_to_jalali(date):
  jalali_date = khayyam.JalaliDate(date)
  return f'{jalali_date.year}-{jalali_date.month}-{jalali_date.day}'


def is_holiday(col):
  year,month,day = (map(int,col.split('-')))
  weekday = khayyam.JalaliDate(year,month,day).weekday()
  return weekday == 6 or weekday == 5 