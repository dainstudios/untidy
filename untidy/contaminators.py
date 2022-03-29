""" Functions to contaminate the data """
import pandas as pd
import numpy as np
import random

""" Column-wise contaminators """

""" Functions to contaminate any columns: """

def nan_values(clean_data, corruption_level = 4):
    """
    Introduce missing values in clean data

    Parameters
    ----------
    clean_data: pd.Series or pd.DataFrame
        data to be contaminated with missing values
    corruption_level: int, optional

    Returns
    -------
    contaminated data as pd.DataFrame

    """
    data = clean_data.copy()
    # get data shape
    if isinstance(data, pd.Series):
        row_idxs = data.shape[0]
        col_idxs = 2

    elif isinstance(data, pd.DataFrame):
        row_idxs, col_idxs = data.shape 
        
    else:
        print('data should be pd.Series, pd.DataFrame or np.ndarray')

    row_idxs = row_idxs-1
    col_idxs = col_idxs-1
    
    # define amount of missing values to introduce
    missing_count = int(row_idxs * col_idxs * corruption_level/10)

    # generate randomized missing values indeces
    nan_idxs = []
    while len(nan_idxs) < missing_count:
        if col_idxs > 1:
            idx_pair = ( random.randint(0, row_idxs), random.randint(0, col_idxs))
        else:
            idx_pair = ( random.randint(0, row_idxs), 0)

        if idx_pair not in nan_idxs:
            nan_idxs.append(idx_pair)

    # insert missing values
    for x, y in nan_idxs:
        if isinstance(data, pd.DataFrame):
            data.iloc[x:x+1, y:y+1] = np.nan
        else:
            data[x] = np.nan
    
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

""" Functions to contaminate string columns: """
