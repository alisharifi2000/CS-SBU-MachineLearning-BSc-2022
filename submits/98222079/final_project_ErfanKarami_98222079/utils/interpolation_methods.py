import jdatetime
from datetime import datetime,timedelta
from scipy.interpolate import interp1d
import pandas as pd
import numpy as np
import math

def interpolation_convert(data ,config):
    result='invalid type config!'
    if config['type']=='shamsi':
        result=shamsi_date_handler(data,config)
    elif config['type']=='miladi':
        result=miladi_date_handler(data,config)
    return result

def persian_interpolat(data ,config):
    result='invalid time config!'
    data['time']=data['time'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d'))
    data['time']=data['time'].apply(lambda x: jdatetime.GregorianToJalali(x.year,x.month,x.day))
    data['time']=data.time.apply(lambda x : f'{x.jyear}-{x.jmonth}-{x.jday}')
    if config['time']=='daily':
        result=day_interpolate(data)
    elif config['time']=='monthly':
        result=month_interpolate(data)
    return result

def shamsi_date_handler(data ,config):
    if config['time']=='daily':
        data['time']=data['time'].apply(lambda x : jdatetime.datetime.strptime(x,'%Y-%m-%d').togregorian())
        data=data.set_index('time')
        data=data.resample(rule='1D').interpolate(method='linear')
        data.reset_index(inplace=True)
        data['time']=data.time.apply(lambda x : jdatetime.GregorianToJalali(x.year,x.month,x.day))
        data['time']=data.time.apply(lambda x : f'{x.jyear}-{x.jmonth}-{x.jday}')
        return data
    elif config['time']=='monthly':
        return month_interpolate(data)
    else:
        return 'invalid time config!'

def miladi_date_handler(data,config):
    if config['time']=='daily':
        data['time']=data['time'].apply(lambda x :datetime.strptime(x,'%Y-%m-%d'))
        data=data.set_index('time')
        data=data.resample(rule='D').interpolate(method='linear')
        data.reset_index(inplace=True)
        data['time']=data.time.apply(lambda x : datetime.strftime(x,'%Y-%m-%d'))
        return data
    elif config['time']=='monthly':
        return month_interpolate(data)
    else:
        return 'invalid time config!'


def date_extractor(data):
    date_list=data.split('-')
    return {
        'year':int(date_list[0]),
        'month':int(date_list[1]),
        'day':int(date_list[2]),
    }


def month_interpolate(data):
    result=data['time'].apply(date_extractor)
    extracted_data=pd.DataFrame.from_records(result)
    extracted_data['vol']=data['vol'].values
    extracted_data=pd.DataFrame(extracted_data.groupby(by=['year','month'])['vol'].sum().values/extracted_data.groupby(by=['year','month']).size()).reset_index()
    years=extracted_data['year'].values
    months=extracted_data['month'].values
    years=years-min(years)
    x=years*12+months
    extracted_data=extracted_data.rename(columns={0:'vol'})
    y=extracted_data['vol'].values
    interpolator=interp1d(x,y)
    new_x=list(range(min(x),max(x)+1))
    new_y=[]
    for i in new_x:
        new_y.append(float(interpolator(i)))
    month=list(map(lambda x:12 if x%12==0 else x%12,new_x))
    min_year=min(extracted_data['year'].values)
    years=[]
    modular=0
    for i in range(len(month)):
        years.append(min_year)
        if month[i]==12:
            modular+=1
    date=list(map(lambda x,y:f'{x}-{y}',years,month))
    result=pd.DataFrame(columns=['time','vol'])
    result['time']=date
    result['vol']=new_y
    return result


def day_interpolate(data):
    date_list=data['time'].apply(lambda x: jdatetime.datetime.strptime(x,'%Y-%m-%d')).values
    vol_list=data['vol'].values
    min_date=min(date_list)
    max_date=max(date_list)
    result_list=[]
    date=min_date
    while True:
        if date in date_list:
            result_list.append({'time':date,'vol':vol_list[np.where(date_list==date)[0][0]]})
        else:
            result_list.append({'time':date,'vol':np.NAN})
        date+=timedelta(days=1)
        if date>max_date:
            break
    result=pd.DataFrame.from_records(result_list)
    result['index']=list(range(len(result)))
    not_null_result=result[result['vol'].notna()]
    interpolator=interp1d(not_null_result['index'].values,not_null_result['vol'].values)
    predicted=list(map(lambda x:float(interpolator(x)),result['index'].values))
    result['vol']=predicted
    result['time']=result['time'].apply(lambda x: f'{x.year}-{x.month}-{x.day}')
    result.drop(columns=['index'],inplace=True)
    return result