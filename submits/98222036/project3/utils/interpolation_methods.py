from datetime import datetime


time_freq_type = {'seconds':'S', 'minutes':'T', 'hours':'H', 'daily':'D', 'monthly':'M', 'yearly':'Y'}

def interpolate(data, config):
    try:
        data = data.set_index('time')
        if ('frequency' in config):
            data = data.resample(str(config['frequency']) + time_freq_type[config['time']])
            # print(str(config['frequency']) + time_freq_type[config['time']])
        else:
            data = data.resample(time_freq_type[config['time']])
        
        if ('interpolation_order' in config):
            data = data.interpolate(method=config['interpolation'], order=config['interpolation_order'])
        else:
            data = data.interpolate(method=config['interpolation'], order=1)
        data.reset_index(inplace=True)

        if ('skip_holiday' in config and config['skip_holiday']):
            tem_time = data.time
            tem_time = tem_time.map(lambda t: t.weekday())
            # print(tem_time)
            data.drop(tem_time.loc[(tem_time == 3) | (tem_time == 4)].index, inplace=True)

    except Exception as e:
        raise e

    return data

"""
{
  "data": {
    "time": {
      "0": 1577836800000,
      "1": 1577923200000,
      "2": 1578096000000
    },
    "vol": {
      "0": 20,
      "1": 40,
      "2": 100
    }
  },
  "confing": {
    "type": "miladi"/"shamsi",
    "time": "seconds/minutes/hours/daily"/"monthly"/"yearly",
    "frequency": 1/2/3/4/5/6/...
    "interpolation": "polynomiyal"/"Spline"
    "interpolation_order": 1/2/3/...
  }
}
"""
