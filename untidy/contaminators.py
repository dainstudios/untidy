""" Functions to contaminate the data """
import pandas as pd
import numpy as np
import random

""" Helpers """


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
        raise TypeError("data should be pd.Series or pd.DataFrame")

    return num_rows, num_cols


def get_random_indices(data, coltype="any", corruption_level=4):
    """
    Get random indeces to contaminate

    Parameters
    ----------
    row_idxs: int
        number of rows in data to contaminate
    col_idxs: int
        number of columns in data to contaminate
    coltype:  str, optional
        type of column
    corruption_level int, optional
        level of corruption, should be between 0 and 10, where 0 leaves the dataset as is, 10
        is the highest level of contamination

    Returns
    -------
    list of indeces to be contaminated
    """

    # define amount of missing values to introduce
    num_obs = data.shape[0] * data.shape[1]
    prop_contaminated = np.linspace(0, 0.6, 11)[corruption_level]
    num_contaminated = int(prop_contaminated * num_obs)

    # generate randomized missing values indeces
    nan_idxs = []
    while len(nan_idxs) < missing_count:
        if col_idxs > 1:
            idx_pair = (
                random.randint(0, row_idxs - 1),
                random.randint(0, col_idxs - 1),
            )
        else:
            idx_pair = (random.randint(0, row_idxs - 1),)

        if idx_pair not in nan_idxs:
            nan_idxs.append(idx_pair)

    return nan_idxs


""" Functions to contaminate text columns """


def add_noise_to_strings(clean_data, corruption_level=4):
    """
    Introduce noise to strings in clean data

    Parameters
    ----------
    clean_data: pd.Series or pd.DataFrame
        data to be contaminated with superfluous characters
    corruption_level: int, optional
        level of corruption, should be between 0 and 10, where 0 leaves the dataset as is, 10
        is the highest level of contamination

    Returns
    -------
    data: pd.DataFrame or pd.Series
        contaminated dataset
    """
    data = clean_data.copy()

    # Find data cells to contaminate
    idxs_to_contaminate = get_random_indices(
        data, col_type="str", corruption_level=corruption_level
    )

    # Perform contamination
    noise_chars = "%&$?!#"
    whitespace = "  "
    for x, y in idxs_to_contaminate:
        # add either extra whitespace or a superfluous character
        noise_char = random.choice(noise_chars)
        noise = random.choice([noise_char, whitespace])
        if isinstance(data, pd.DataFrame):
            data.iloc[x, y] += noise
        else:
            data[x] += noise

    return data


def change_str_encoding(clean_data, corruption_level=4):
    """
    Changes the string encoding of text data.

    Parameters
    ----------
    clean_data: pd.Series or pd.DataFrame
        data to be contaminated with superfluous characters
    corruption_level: int, optional
        level of corruption, should be between 0 and 10, where 0 leaves the dataset as is, 10
        is the highest level of contamination

    Returns
    -------
    data: pd.DataFrame or pd.Series
        contaminated dataset
    """
    data = clean_data.copy()

    if isinstance(data, pd.DataFrame):
        # Find random columns to contaminate
        str_cols = list(data.select_dtypes(include=["object"]).columns)
        num_str_cols = len(str_cols)
        possible_num_cols_to_contaminate = [
            int(np.ceil(n)) for n in np.linspace(0, int(num_str_cols) / 2, 11)
        ]
        num_cols_to_contaminate = possible_num_cols_to_contaminate[corruption_level]
        cols_to_contaminate = list(
            np.random.choice(str_cols, num_cols_to_contaminate, replace=False)
        )

        # Change encoding of columns
        for col in cols_to_contaminate:
            if corruption_level > 8:
                data[col] = data[col].str.encode("utf-16")
            else:
                data[col] = data[col].str.encode("ascii")

    elif isinstance(data, pd.Series):
        if corruption_level > 8:
            data = data.str.encode("utf-16")
        else:
            data = data.str.encode("ascii")
    else:
        raise ValueError("'clean_data' should be either a pd.DataFrame or pd.Series")

    return data


def add_nans(clean_data, corruption_level=4):
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

    nan_idxs = get_random_indices(num_rows, num_cols, corruption_level=corruption_level)

    # insert missing values
    for x, y in nan_idxs:
        if isinstance(data, pd.DataFrame):
            data.iloc[x : x + 1, y : y + 1] = np.nan
        else:
            data[x] = np.nan

    print(data)
    return data


""" Functions to contaminate numerical columns """


def change_numeric_to_str(clean_data, corruption_level=4):
    """
    Changes the dtype in some numeric columns to strings

    Parameters
    ----------
    clean_data: pd.Series or pd.DataFrame
        data to be contaminated with superfluous characters
    corruption_level: int, optional
        level of corruption, should be between 0 and 10, where 0 leaves the dataset as is, 10
        is the highest level of contamination

    Returns
    -------
    data: pd.DataFrame or pd.Series
        contaminated dataset
    """
    data = clean_data.copy()

    if isinstance(data, pd.DataFrame):
        # Find random columns to contaminate
        numeric_cols = list(data.select_dtypes(include=["float64", "in64"]).columns)
        num_numeric_cols = len(numeric_cols)
        possible_num_cols_to_contaminate = [
            int(np.ceil(n)) for n in np.linspace(0, int(num_numeric_cols) / 2, 11)
        ]
        num_cols_to_contaminate = possible_num_cols_to_contaminate[corruption_level]
        cols_to_contaminate = list(
            np.random.choice(numeric_cols, num_cols_to_contaminate, replace=False)
        )

        # Change dtype of columns
        for col in cols_to_contaminate:
            data[col] = data[col].astype(str)

    elif isinstance(data, pd.Series):
        data = data.astype(str)

    else:
        raise ValueError("'clean_data' should be either a pd.DataFrame or pd.Series")

    return data


""" Functions to contaminate any column """


def nan_values(clean_data, corruption_level=4):
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

    nan_idxs = random_indices(row_idxs, col_idxs, corruption_level=corruption_level)

    # insert missing values
    for x, y in nan_idxs:
        if isinstance(data, pd.DataFrame):
            data.iloc[x : x + 1, y : y + 1] = np.nan
        else:
            data[x] = np.nan

    return data


def add_outliers(clean_data, corruption_level=4):
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

    # data_raw = clean_data.copy()
    data = clean_data.copy()

    print(data)

    # get numerical columns
    if isinstance(data, pd.DataFrame):
        numeric_col = list(data.select_dtypes(include=np.number).columns)
        data = data[numeric_col]
        num_limits = {col: (data[col].min(), data[col].max()) for col in numeric_col}
    else:
        num_limits = (data.min(), data.max())

    # get data shape
    num_rows, num_cols = get_data_dims(data)

    ol_idxs = get_random_indices(num_rows, num_cols, corruption_level=corruption_level)

    # random sign function
    coin_flip = lambda: 1 if random.random() > 0.5 else -1

    # contaminate data
    for x, y in ol_idxs:

        coin = coin_flip()
        if coin > 0:
            # +100 times the max(1, max_value)
            if isinstance(data, pd.DataFrame):
                data.iloc[x : x + 1, y : y + 1] = (
                    num_limits[numeric_col[y]][1]
                    + max(num_limits[numeric_col[y]][1], 1) * 1000
                )
            else:
                data[x] = num_limits[1] + max(1, num_limits[1]) * 1000
        else:
            # - 100 times min(-1, min_value)
            if isinstance(data, pd.DataFrame):
                data.iloc[x : x + 1, y : y + 1] = (
                    num_limits[numeric_col[y]][0]
                    - max(num_limits[numeric_col[y]][0], 1) * 1000
                )
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
