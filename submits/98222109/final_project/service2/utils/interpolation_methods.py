import pandas as pd
import dask
import dask.dataframe as dd

def linear_interpolation(data, config):
    if config['time'] == 'daily':
        data = data.set_index('time')
        data = data.resample('D').mean()
        if(config['tool'] == 'Pandas'):
            data = data.interpolate(method=config['interpolation'])
        elif(config['tool'] == 'Dask'):
            data = dd.from_pandas(data.compute().interpolate(method=config['interpolation']), npartitions=10)
        if (config['tool'] == 'Pandas'):
            data.reset_index(inplace = True)
        elif (config['tool'] == 'Dask'):
            data = data.compute().reset_index()

    elif config['time'] == 'monthly':
        data = data.set_index('time')
        data = data.resample('M').mean()
        if (config['tool'] == 'Pandas'):
            data = data.interpolate(method=config['interpolation'])
        elif (config['tool'] == 'Dask'):
            data = dd.from_pandas(data.compute().interpolate(method=config['interpolation']), npartitions=10)
        if (config['tool'] == 'Pandas'):
            data.reset_index(inplace=True)
        elif (config['tool'] == 'Dask'):
            data = data.compute().reset_index()

    elif(config['time'] == 'hourly'):
        data = data.set_index('time')
        data = data.resample('1H').mean()
        if (config['tool'] == 'Pandas'):
            data = data.interpolate(method=config['interpolation'])
        elif (config['tool'] == 'Dask'):
            data = dd.from_pandas(data.compute().interpolate(method=config['interpolation']), npartitions=10)
        if (config['tool'] == 'Pandas'):
            data.reset_index(inplace=True)
        elif (config['tool'] == 'Dask'):
            data = data.compute().reset_index()

    elif(config['time'] == 'minutes'):
        data = data.set_index('time')
        data = data.resample('1T').mean()
        if (config['tool'] == 'Pandas'):
            data = data.interpolate(method=config['interpolation'])
        elif (config['tool'] == 'Dask'):
            data = dd.from_pandas(data.compute().interpolate(method=config['interpolation']), npartitions=10)
        if (config['tool'] == 'Pandas'):
            data.reset_index(inplace=True)
        elif (config['tool'] == 'Dask'):
            data = data.compute().reset_index()

    elif(config['time'] == 'seconds'):
        data = data.set_index('time')
        data = data.resample('1S').mean()
        if (config['tool'] == 'Pandas'):
            data = data.interpolate(method=config['interpolation'])
        elif (config['tool'] == 'Dask'):
            data = dd.from_pandas(data.compute().interpolate(method=config['interpolation']), npartitions=10)
        if (config['tool'] == 'Pandas'):
            data.reset_index(inplace=True)
        elif (config['tool'] == 'Dask'):
            data = data.compute().reset_index()

    else:
        data = None

    return data


def polynomial_interpolation(data, config):
    if config['time'] == 'daily':
        data = data.set_index('time')
        data = data.resample('D').mean()
        if (config['tool'] == 'Pandas'):
            data = data.interpolate(method=config['interpolation'], order = 2)
        elif (config['tool'] == 'Dask'):
            data = dd.from_pandas(data.compute().interpolate(method=config['interpolation'], order = 2), npartitions=10)
        if (config['tool'] == 'Pandas'):
            data.reset_index(inplace=True)
        elif (config['tool'] == 'Dask'):
            data = data.compute().reset_index()

    elif config['time'] == 'monthly':
        data = data.set_index('time')
        data = data.resample('M').mean()
        if (config['tool'] == 'Pandas'):
            data = data.interpolate(method=config['interpolation'], order = 2)
        elif (config['tool'] == 'Dask'):
            data = dd.from_pandas(data.compute().interpolate(method=config['interpolation'], order = 2), npartitions=10)
        if (config['tool'] == 'Pandas'):
            data.reset_index(inplace = True)
        elif (config['tool'] == 'Dask'):
            data = data.compute().reset_index()

    elif (config['time'] == 'hourly'):
        data = data.set_index('time')
        data = data.resample('1H').mean()
        if (config['tool'] == 'Pandas'):
            data = data.interpolate(method=config['interpolation'], order = 2)
        elif (config['tool'] == 'Dask'):
            data = dd.from_pandas(data.compute().interpolate(method=config['interpolation'], order = 2), npartitions=10)
        if (config['tool'] == 'Pandas'):
            data.reset_index(inplace=True)
        elif (config['tool'] == 'Dask'):
            data = data.compute().reset_index()

    elif (config['time'] == 'minutes'):
        data = data.set_index('time')
        data = data.resample('1T').mean()
        if (config['tool'] == 'Pandas'):
            data = data.interpolate(method=config['interpolation'], order = 2)
        elif (config['tool'] == 'Dask'):
            data = dd.from_pandas(data.compute().interpolate(method=config['interpolation'], order = 2), npartitions=10)
        if (config['tool'] == 'Pandas'):
            data.reset_index(inplace=True)
        elif (config['tool'] == 'Dask'):
            data = data.compute().reset_index()

    elif (config['time'] == 'seconds'):
        data = data.set_index('time')
        data = data.resample('1S').mean()
        if (config['tool'] == 'Pandas'):
            data = data.interpolate(method=config['interpolation'], order = 2)
        elif (config['tool'] == 'Dask'):
            data = dd.from_pandas(data.compute().interpolate(method=config['interpolation'], order = 2), npartitions=10)
        if (config['tool'] == 'Pandas'):
            data.reset_index(inplace=True)
        elif (config['tool'] == 'Dask'):
            data = data.compute().reset_index()

    else:
        data = None

    return data


def spline_interpolation(data, config):
    if config['time'] == 'daily':
        data = data.set_index('time')
        data = data.resample('D').mean()
        if (config['tool'] == 'Pandas'):
            data = data.interpolate(method=config['interpolation'], order = 2)
        elif (config['tool'] == 'Dask'):
            data = dd.from_pandas(data.compute().interpolate(method=config['interpolation'], order = 2), npartitions=10)
        if (config['tool'] == 'Pandas'):
            data.reset_index(inplace=True)
        elif (config['tool'] == 'Dask'):
            data = data.compute().reset_index()

    elif config['time'] == 'monthly':
        data = data.set_index('time')
        data = data.resample('M').mean()
        if (config['tool'] == 'Pandas'):
            data = data.interpolate(method=config['interpolation'], order = 2)
        elif (config['tool'] == 'Dask'):
            data = dd.from_pandas(data.compute().interpolate(method=config['interpolation'], order = 2), npartitions=10)
        if (config['tool'] == 'Pandas'):
            data.reset_index(inplace=True)
        elif (config['tool'] == 'Dask'):
            data = data.compute().reset_index()

    elif (config['time'] == 'hourly'):
        data = data.set_index('time')
        data = data.resample('1H').mean()
        if (config['tool'] == 'Pandas'):
            data = data.interpolate(method=config['interpolation'], order = 2)
        elif (config['tool'] == 'Dask'):
            data = dd.from_pandas(data.compute().interpolate(method=config['interpolation'], order = 2), npartitions=10)
        if (config['tool'] == 'Pandas'):
            data.reset_index(inplace=True)
        elif (config['tool'] == 'Dask'):
            data = data.compute().reset_index()

    elif (config['time'] == 'minutes'):
        data = data.set_index('time')
        data = data.resample('1T').mean()
        if (config['tool'] == 'Pandas'):
            data = data.interpolate(method=config['interpolation'], order = 2)
        elif (config['tool'] == 'Dask'):
            data = dd.from_pandas(data.compute().interpolate(method=config['interpolation'], order = 2), npartitions=10)
        if (config['tool'] == 'Pandas'):
            data.reset_index(inplace=True)
        elif (config['tool'] == 'Dask'):
            data = data.compute().reset_index()

    elif (config['time'] == 'seconds'):
        data = data.set_index('time')
        data = data.resample('1S').mean()
        if (config['tool'] == 'Pandas'):
            data = data.interpolate(method=config['interpolation'], order = 2)
        elif (config['tool'] == 'Dask'):
            data = dd.from_pandas(data.compute().interpolate(method=config['interpolation'], order = 2), npartitions=10)
        if (config['tool'] == 'Pandas'):
            data.reset_index(inplace=True)
        elif (config['tool'] == 'Dask'):
            data = data.compute().reset_index()

    else:
        data = None

    return data
