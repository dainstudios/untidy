""" Functions to contaminate the data """
import pandas as pd
import numpy as np
import random

""" Column-wise contaminators """

def get_data_dims(data):
    """
    Check input data

    Params
    ------
    data: pd.Series, pd.DataFrame
        data to check

    Returns
    -------
    num_rows, num_cols: int(s)
        integers specifying, respectively, the amount of rows and columns in data.
        These values will be passed to *random_indeces* in order to generate the indeces to be contaminated

    """
    if isinstance(data, pd.Series):
        num_rows = data.shape[0]
        num_cols = 1

    elif isinstance(data, pd.DataFrame):
        num_rows, num_cols = data.shape 
        
    else:
        raise TypeError('data should be pd.Series or pd.DataFrame')

    return num_rows, num_cols

def get_random_indices(num_rows, num_cols, corruption_level = 4):
    """
    Get random indeces to contaminate

    Parameters
    ----------
    num_rows: int
        number of rows in data to contaminate
    num_cols: int
        number of columns in data to contaminate
    corruption_level int, optional
        level of corruption, should be between 0 and 10, where 0 leaves the dataset as is, 10
        is the highest level of contamination

    Returns
    -------
    list of indeces to be contaminated
    """

    # define amount of missing values to introduce
    contamination_fraction = round(num_rows * num_cols * corruption_level/10 * 0.6)

    # generate randomized missing values indeces
    
    if num_cols>1:
        cont_idxs = zip(random.choices(range(num_rows), k=contamination_fraction),
                    random.choices(range(num_cols), k=contamination_fraction))
    else:
        cont_idxs = zip(random.choices(range(num_rows), k=contamination_fraction),
                    [0 for i in range(contamination_fraction)])

    return cont_idxs



""" Functions to contaminate any columns: """

def add_nans(clean_data, corruption_level = 4):
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
    contaminated data as pd.DataFrame or pd.Series

    """
    data = clean_data.copy()
    print(data)
    
    num_rows, num_cols = get_data_dims(data)

    nan_idxs = get_random_indices(num_rows, num_cols, corruption_level = corruption_level)
    
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

    #data_raw = clean_data.copy()
    data = clean_data.copy()

    print(data)

    # get numerical columns
    if isinstance(data, pd.DataFrame):
        numeric_col = list(data.select_dtypes(include = np.number).columns)
        data = data[numeric_col]
        num_limits = {col:(data[col].min(),data[col].max()) for col in numeric_col}
    else:
        num_limits = (data.min(), data.max())

    # get data shape
    num_rows, num_cols = get_data_dims(data)

    ol_idxs = get_random_indices(num_rows, num_cols, corruption_level = corruption_level)
     
    # random sign function
    coin_flip = lambda: 1 if random.random() > 0.5 else -1
    
    # contaminate data
    for x, y in ol_idxs:

        coin = coin_flip()
        if coin>0:
            # +100 times the max(1, max_value)
            if isinstance(data, pd.DataFrame):
                data.iloc[x:x+1, y:y+1] = num_limits[numeric_col[y]][1] + max(num_limits[numeric_col[y]][1], 1) * 1000
            else:
                data[x] = num_limits[1] + max(1, num_limits[1]) * 1000
        else:
            # - 100 times min(-1, min_value)
            if isinstance(data, pd.DataFrame):
                data.iloc[x:x+1, y:y+1] = num_limits[numeric_col[y]][0] - max(num_limits[numeric_col[y]][0], 1) * 1000
            else:
                data[x] = num_limits[0] - max(num_limits[0], 1) * 1000

    # add contamination to original dataframe
    
    if isinstance(data, pd.DataFrame):
        data_contaminated = clean_data.copy()
        data_contaminated[numeric_col] = data[numeric_col]
    else:
        data_contaminated = data
    
    print(data_contaminated)

    return data_contaminated

    """ Functions to contaminate string columns: """