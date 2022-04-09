import math

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
        
    df['baseRent'].fillna(0, inplace=True)
    df['heatingCosts'].fillna(0, inplace=True)
    df['serviceCharge'].fillna(0, inplace=True)
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
    df.drop(df.loc[((df['totalRent'] < 250) | (df['totalRent'] > 3300))].index,
            inplace=True, axis=0)

    df['floor_division'] = df['floor'] / df['numberOfFloors'] 
    df['meter_price'] = df['baseRent'] / df['livingSpace']

    drop_cols = ["houseNumber", "geo_krs", "geo_bln", "street",
                 "noRooms", "livingSpace", "baseRent",
                 "energyEfficiencyClass", "yearConstructedRange",
                 "telekomHybridUploadSpeed", "date",
                 "electricityBasePrice", "electricityKwhPrice",
                 "serviceCharge", "heatingCosts", "lastRefurbish"]

    df.drop(drop_cols, inplace=True, axis=1)

    df.drop_duplicates(keep='first', inplace=True)

    print("Shape dataframe before drop section: ", pre_size_df)
    print("Shape dataframe after drop section: ", df.shape)
    print(f"{pre_size_df[0] - df.shape[0]} instances were droped. \
          ({((pre_size_df[0] - df.shape[0]) / pre_size_df[0]) * 100 } % of the whole dataset.) \
          {len(drop_cols)} columns were droped, and 2 were added.")

    df.set_index('scoutId', inplace=True)

    return df