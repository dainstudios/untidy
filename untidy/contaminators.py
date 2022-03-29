""" Functions to contaminate the data """
import pandas as pd
import numpy as np
import random

""" Column-wise contaminators """

def data_check(data):
    """
    Check input data

    Params
    ------
    data: pd.Series, pd.DataFrame
        data to check

    Returns
    -------
    row_idxs, col_idxs: int(s)
        integers specifying, respectively, the amount of rows and columns in data.
        These values will be passed to *random_indeces* in order to generate the indeces to be contaminated

    """
    if isinstance(data, pd.Series):
        row_idxs = data.shape[0]
        col_idxs = 2

    elif isinstance(data, pd.DataFrame):
        row_idxs, col_idxs = data.shape 
        
    else:
        raise TypeError('data should be pd.Series or pd.DataFrame')

    return row_idxs, col_idxs

def random_indices(row_idxs, col_idxs, corruption_level = 4):
    """
    Get random indeces to contaminate

    Parameters
    ----------
    row_idxs: int
        number of rows in data to contaminate
    col_idxs: int
        number of columns in data to contaminate
    corruption_level int, optional
        level of corruption, should be between 0 and 10, where 0 leaves the dataset as is, 10
        is the highest level of contamination

    Returns
    -------
    list of indeces to be contaminated
    """

    # define amount of missing values to introduce
    missing_count = int(row_idxs * col_idxs * corruption_level/10)

    # generate randomized missing values indeces
    nan_idxs = []
    while len(nan_idxs) < missing_count:
        if col_idxs > 1:
            idx_pair = (random.randint(0, row_idxs-1), random.randint(0, col_idxs-1))
        else:
            idx_pair = (random.randint(0, row_idxs-1), )

        if idx_pair not in nan_idxs:
            nan_idxs.append(idx_pair)

    return nan_idxs



""" Functions to contaminate any columns: """

def nan_values(clean_data, corruption_level = 4):
    """
    Introduce missing values in clean data

    Parameters
    ----------
    clean_data: pd.Series or pd.DataFrame
        data to be contaminated with missing values
    corruption_level: int, optional
        level of corruption, should be between 0 and 10, where 0 leaves the dataset as is, 10
        is the highest level of contamination

    Returns
    -------
    contaminated data as pd.DataFrame

    """
    data = clean_data.copy()
    
    row_idxs, col_idxs = data_check(data)

    nan_idxs = random_indices(row_idxs, col_idxs, corruption_level = corruption_level)

    # insert missing values
    for x, y in nan_idxs:
        if isinstance(data, pd.DataFrame):
            data.iloc[x:x+1, y:y+1] = np.nan
        else:
            data[x] = np.nan

    print(data)
    return data


def contaminate_strings_with_noise(a, corruption_level=4):
    """
    Contaminate an array with extra characters.

    Parameters
    ----------
    a: np.array, pd.Series or list
        column of the dataset to be contaminated
    corruption_level: int, optional
        level of corruption, should be between 0 and 10, where 0 leaves the dataset as is, 10
        is the highest level of contamination
    """
    a_contaminated = a.copy()

    # Perform contamination

    return a_contaminated


""" Functions to contaminate numerical columns: """
def add_outliers(clean_data, corruption_level = 4):
    """
    Contaminate data with obvious outliers

    Parameters
    ----------
    clean_data: pd.Series or pd.DataFrame
        data to be contaminated with missing values
    corruption_level: int, optional

    Returns
    -------
    contaminated data as pd.DataFrame

    """

    data_raw = clean_data.copy()
    data = data_raw.copy()

    # get numerical columns
    if isinstance(data, pd.DataFrame):
        num_cols = list(data.select_dtypes(include = np.number).columns)
        data = data[num_cols]
        num_limits = {col:(data[col].min(),data[col].max()) for col in num_cols}
    else:
        num_limits = (data.min(), data.max())

    # get data shape
    row_idxs, col_idxs = data_check(data)

    nan_idxs = random_indices(row_idxs, col_idxs, corruption_level = corruption_level)
 
    # random sign function
    coin_flip = lambda: 1 if random.random() > 0.5 else -1
    
    # contaminate data
    for x, y in nan_idxs:

        coin = coin_flip()

        if coin>0:
            # +/- 100 times the max
            if isinstance(data, pd.DataFrame):
                data.iloc[x:x+1, y:y+1] = coin_flip() * num_limits[num_cols[y]][1] * 100
            else:
                data[x] = coin_flip() * num_limits[1] * 100
        else:
            # +/- 100 times the min
            if isinstance(data, pd.DataFrame):
                data.iloc[x:x+1, y:y+1] = coin_flip() * num_limits[num_cols[y]][0] * 100
            else:
                data[x] = coin_flip() * num_limits[0] * 100

    # add contamination to original dataframe
    if isinstance(data, pd.DataFrame):
        data_raw[num_cols] = data[num_cols]
    else:
        data_raw = data
        
    print(data_raw)
    return data_raw


""" Functions to contaminate string columns: """
