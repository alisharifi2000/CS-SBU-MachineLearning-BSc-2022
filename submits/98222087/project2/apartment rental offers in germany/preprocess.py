import math
import pandas as pd
import numpy as np


def data_cleaner(df):
    '''
    Drops irrational instances, columns, and duplicates, fills missing values
    Arguments:
        df is a n-by-d pandas data frame
    Returns:
        the final dataframe 
    '''
    
    pre_size_df = df.shape
      
    df.drop(df.loc[df['noRooms'] > 10].index, inplace=True, axis=0)
    df.drop(df.loc[df['noParkSpaces'] > 4].index, inplace=True, axis=0)
    df.drop(df.loc[df['thermalChar'] > 350].index, inplace=True, axis=0)
    df.drop(df.loc[df['baseRent'] > 3000].index, inplace=True, axis=0)
    df.drop(df.loc[df['livingSpace'] > 250].index, inplace=True, axis=0)
    df.drop(df.loc[((df['livingSpace'] < 18) |
                    (df['livingSpace'] > 250))].index, inplace=True, axis=0)
    df.drop(df.loc[(df['lastRefurbish'] > 2021) |
            (df['lastRefurbish'] < 1950)].index, inplace=True, axis=0)
    df.drop(df.loc[(df['floor'] > 10) |
            (df['floor'] < 0)].index, inplace=True, axis=0)
    df.drop(df.loc[(df['numberOfFloors'] > 12) |
            (df['numberOfFloors'] < 1)].index, inplace=True, axis=0)
    df.drop(df.loc[((df['yearConstructed'] < 1850) |
                    (df['yearConstructed'] > 2022))].index, inplace=True, axis=0)
    df.drop(df.loc[df['picturecount'] > 40].index, inplace=True, axis=0)
        
    df['baseRent'].fillna(value=df['baseRent'].mean(), inplace=True) # changed from 0 to mean
    df['heatingCosts'].fillna(value=df['heatingCosts'].mean(), inplace=True) # changed from 0 to mean
    df['serviceCharge'].fillna(value=df['serviceCharge'].mean(), inplace=True) # changed from 0 to mean
    df['totalRent'].fillna(df['baseRent'] + df['serviceCharge'] + df['heatingCosts'], 
                           inplace=True) #based on the data documentation
    df['heatingType'].fillna(value='no_heating', inplace=True)
    df['telekomTvOffer'].fillna(value='NO_INFO', inplace=True)
    df['telekomUploadSpeed'].fillna(value=0, inplace=True)
    df['noParkSpaces'].fillna(value=0, inplace=True)
    df['firingTypes'].fillna(value=df['firingTypes'].value_counts().index[0], inplace=True)
    df['petsAllowed'].fillna(value=df['petsAllowed'].value_counts().index[0], inplace=True)
    df['typeOfFlat'].fillna(value=df['typeOfFlat'].value_counts().index[0], inplace=True)
    df['thermalChar'].fillna(value=df['thermalChar'].mean(), inplace=True)
    df['numberOfFloors'].fillna(value=df['numberOfFloors'].mean().round(0), inplace=True)
    df['floor'].fillna(value=df['floor'].mean().round(0), inplace=True)
    df['pricetrend'].fillna(value=df['pricetrend'].mean(), inplace=True)
    df['condition'].fillna('other', inplace=True)
    df['yearConstructed'].fillna(df.groupby('condition')['yearConstructed'].\
                                 transform('mean').round(0), inplace=True)
    df['interiorQual'].fillna('other', inplace=True)
    df['streetPlain'].fillna('other', inplace=True)
    df['description'].fillna('other', inplace=True)
    df['facilities'].fillna('other', inplace=True)

    df['has_refurbished'] = df['lastRefurbish'].apply(lambda x: False if math.isnan(x) else True)
    

    df.drop(df.loc[df['telekomTvOffer'].isna()].index, inplace=True, axis=0)
    df.drop(df.loc[df['totalRent'].isna()].index, inplace=True, axis=0)        
    df.drop(df.loc[df['serviceCharge'].isna()].index, inplace=True, axis=0) # added        
    df.drop(df.loc[((df['totalRent'] < 250) | (df['totalRent'] > 3300))].index,
            inplace=True, axis=0)

    df['floor_division'] = df['floor'] / df['numberOfFloors'] 
    df['meter_price'] = df['baseRent'] / df['livingSpace']

    df.drop(df.loc[df['floor_division'] > 3.5].index, inplace=True)
    df.drop(df.loc[df['meter_price'] > 33].index, inplace=True)

    drop_cols = ["houseNumber", "geo_krs", "geo_bln", "street",
                 "noRooms", "livingSpace", "baseRent",
                 "energyEfficiencyClass", "yearConstructedRange",
                 "telekomHybridUploadSpeed", "date",
                 "electricityBasePrice", "electricityKwhPrice",
                 "heatingCosts", "lastRefurbish"] # ServiceCharge removed.

    df.drop(drop_cols, inplace=True, axis=1)

    df.drop_duplicates(keep='first', inplace=True)

    print("Shape dataframe before drop section: ", pre_size_df)
    print("Shape dataframe after drop section: ", df.shape)
    print(f"{pre_size_df[0] - df.shape[0]} instances were droped. \
          ({((pre_size_df[0] - df.shape[0]) / pre_size_df[0]) * 100 } % of the whole dataset.) \
          {len(drop_cols)} columns were droped, and 2 were added.")

    df.set_index('scoutId', inplace=True)

    return df

def handle_categorical_vars(df):
    '''
    Apply one hot encoder to nominal variables, maps ordinal variables with custom mapping
    Arguments:
        df is a n-by-d pandas data frame
    Returns:
        the final dataframe 
    '''

    #nominal vars
    df.loc[df['regio1'].isin(['Hamburg', 'Bremen', 'Saarland']), 'regio1'] = 'other'
    df.loc[df['heatingType'].isin(['oil_heating', 'heat_pump', 'combined_heat_and_power_plant',
                                  'night_storage_heater', 'wood_pellet_heating',
                                  'electric_heating', 'stove_heating', 'solar_heating']),
                                  'heatingType'] = 'other'
    df.loc[df['typeOfFlat'].isin(['half_basement', 'loft']), 'typeOfFlat'] = 'bad_flat'

    cols = ['regio1', 'heatingType', 'typeOfFlat']
    dummy_df = pd.get_dummies(df[cols])
    df = pd.concat([df, dummy_df], axis=1)
    df.drop(cols, inplace=True, axis=1)

    #ordinal vars
    telekomTvOffer_dict = {
        'ONE_YEAR_FREE': 2,
        'NO_INFO':1,
        'NONE':0,              
        'ON_DEMAND':1,         
    }
    df['telekomTvOffer'] = df.telekomTvOffer.map(telekomTvOffer_dict)
    
    condition_dict = {
        'other': 2,                                 
        'well_kept': 3,                             
        'refurbished': 1,                           
        'fully_renovated': 3,                        
        'first_time_use': 4,                         
        'mint_condition': 4,                         
        'modernized': 5,                              
        'first_time_use_after_refurbishment': 2,     
        'negotiable': 2,                             
        'need_of_renovation': 0,                     
        'ripe_for_demolition': 0,                    
    }
    df['condition'] = df.condition.map(condition_dict)

    interiorQual_dict = {
        'other': 1,            
        'normal': 2,           
        'sophisticated': 0,    
        'luxury': 3,            
        'simple': 1,           
    }
    df['interiorQual'] = df.interiorQual.map(interiorQual_dict)

    petsAllowed_dict = {
        'negotiable': 1,    
        'no': 0,            
        'yes': 2,            
    }
    df['petsAllowed'] = df.petsAllowed.map(petsAllowed_dict)
                    
    return df

def reduce_mem_usage(df, int_cast=True, obj_to_category=False, subset=None):
    """
    Iterate through all the columns of a dataframe and modify the data type to reduce memory usage.
    :param df: dataframe to reduce (pd.DataFrame)
    :param int_cast: indicate if columns should be tried to be casted to int (bool)
    :param obj_to_category: convert non-datetime related objects to category dtype (bool)
    :param subset: subset of columns to analyse (list)
    :return: dataset with the column dtypes adjusted (pd.DataFrame)
    """
    start_mem = df.memory_usage().sum() / 1024 ** 2;
    print('Memory usage of dataframe is {:.2f} MB'.format(start_mem))
    
    for col in df.columns:
        col_type = df[col].dtype

        if col_type != object and col_type.name not in ['category', 'bool'] and 'datetime' not in col_type.name:
            c_min = df[col].min()
            c_max = df[col].max()

            # test if column can be converted to an integer
            treat_as_int = str(col_type)[:3] == 'int'

            if treat_as_int:
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.uint8).min and c_max < np.iinfo(np.uint8).max:
                    df[col] = df[col].astype(np.uint8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.uint16).min and c_max < np.iinfo(np.uint16).max:
                    df[col] = df[col].astype(np.uint16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.uint32).min and c_max < np.iinfo(np.uint32).max:
                    df[col] = df[col].astype(np.uint32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
                elif c_min > np.iinfo(np.uint64).min and c_max < np.iinfo(np.uint64).max:
                    df[col] = df[col].astype(np.uint64)
            elif str(col_type)[:4] == 'uint':
                pass
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
        elif 'datetime' not in col_type.name and obj_to_category:
            df[col] = df[col].astype('category')
    end_mem = df.memory_usage().sum() / 1024 ** 2
    print('Memory usage after optimization is: {:.3f} MB'.format(end_mem))
    print('Decreased by {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))

    return df

def drop_str_vars(df):
    '''
    Drops remained object variables from the dataset
    Arguments:
        df is a n-by-d pandas data frame
    Returns:
        the final dataframe 
    '''
    
    cols = []
    for col in df.columns:
        name = df[col].dtype.name
        if name == "object":
            cols.append(col)

    df.drop(cols, inplace=True, axis=1)
    return df  