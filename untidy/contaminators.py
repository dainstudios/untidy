import pandas as pd

""" Functions to contaminate the data """
import pandas as pd
import numpy as np
import random

""" Helpers """


def get_random_cols(data, col_type="any", corruption_level=4):
    """
    Get random columns to contaminate

    Parameters
    ----------
    data: pd.DataFrame
        clean dataset
    col_type: str, optional
        'str', 'numeric' or 'any'. Type of columns to sample.
    corruption_level int, optional
        level of corruption, should be between 0 and 10, where 0 leaves the dataset as is, 10
        is the highest level of contamination

    Returns
    -------
    cols: list
        list of columns to be contaminated
    """
    if col_type.startswith("num"):
        col_type = "num"

    # Helpers lambda for sampling columns
    sampling_cols = lambda data, col_types: [
        list(data.columns).index(col)
        for col in data.select_dtypes(include=col_types).columns
    ]
    type_dict = {"str": ["object"], "num": ["float64", "int64"]}

    # Select columns to sample
    if col_type in ["any", "all"]:
        cols_to_sample = list(range(len(data.columns)))
    else:
        cols_to_sample = sampling_cols(data, type_dict[col_type])
    # Find the number of columns to contaminate
    num_contaminated = [
        int(np.ceil(n)) for n in np.linspace(0, int(len(cols_to_sample)) / 2, 11)
    ][corruption_level]

    # Sample columns
    cols = random.choices(cols_to_sample, k=num_contaminated)

    return cols


def get_random_indices(data, col_type="any", corruption_level=4):
    """
    Get random indeces to contaminate

    Parameters
    ----------
    data: pd.DataFrame
        clean dataset
    col_type: str, optional
        'str', 'numeric' or 'any'. Type of columns to sample.
    corruption_level int, optional
        level of corruption, should be between 0 and 10, where 0 leaves the dataset as is, 10
        is the highest level of contamination

    Returns
    -------
    idxs: list
        list of indeces to be contaminated
    """

    # Define the number of datapoints to contaminate
    num_obs = data.values.reshape(1, -1).shape[1]
    prop_contaminated = np.linspace(0, 0.6, 11)[corruption_level]
    num_contaminated = int(prop_contaminated * num_obs)

    # Helpers lambda for sampling columns
    sampling_cols = lambda data, col_types: [
        list(data.columns).index(col)
        for col in data.select_dtypes(include=col_types).columns
    ]
    type_dict = {"str": ["object", "category"], "num": ["float64", "int64"]}

    if isinstance(data, pd.DataFrame):
        # Find columns to sample from
        if col_type in ["any", "all"]:
            cols_to_sample = list(range(len(data.columns)))
        else:
            cols_to_sample = sampling_cols(data, type_dict[col_type])
        sampled_col_idx = random.choices(cols_to_sample, k=num_contaminated)
        sampled_row_idx = random.choices(list(range(len(data))), k=num_contaminated)
        idx = list(set(zip(sampled_row_idx, sampled_col_idx)))
    elif isinstance(data, pd.Series):
        idx = list(data.sample(n=num_contaminated).index)
    else:
        raise TypeError("data should be pd.Series or pd.DataFrame")

    return idx


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
    noise_chars = "%&$?!# "

    for idx in idxs_to_contaminate:
        # Add a superfluous character
        noise = random.choice(noise_chars)
        data.iloc[idx] = str(data.iloc[idx]).replace("nan", "") + noise

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
        cols_to_contaminate = get_random_cols(col_type="str")

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
        raise ValueError("clean_data' should be either a pd.DataFrame or pd.Series")

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
        cols_to_contaminate = get_random_cols(col_type="numeric")

        # Change dtype of columns
        for col in cols_to_contaminate:
            data[col] = data[col].astype(str)

    elif isinstance(data, pd.Series):
        data = data.astype(str)

    else:
        raise ValueError("'clean_data' should be either a pd.DataFrame or pd.Series")

    return data


def add_outliers(clean_data, corruption_level=4):
    """
    Contaminate data with obvious outliers

    Parameters
    ----------
    clean_data: pd.Series or pd.DataFrame
        data to be contaminated with missing values
    corruption_level: int, optional
        level of corruption, should be between 0 and 10, where 0 leaves the dataset as is, 10
        is the highest level of contamination

    Returns
    -------
    data: pd.DataFrame or pd.Series
        contaminated dataset
    """
    data = clean_data.copy()

    # Find magnitude for numeric columns (ie number of zeros in the range of the variable)
    if isinstance(data, pd.DataFrame):
        numeric_cols = list(data.select_dtypes(include=np.number).columns)
        magnitudes = {
            col: np.ceil(np.log10((data[col].max() - data[col].min())))
            for col in numeric_cols
        }
    elif isinstance(data, pd.Series):
        magnitudes = np.ceil(np.log10((data.max() - data.min())))
    else:
        raise TypeError("clean_data should be pd.Series or pd.DataFrame")

    # Find data cells to contaminate
    idxs_to_contaminate = get_random_indices(
        data, col_type="numeric", corruption_level=corruption_level
    )

    # Add outliers - add leading zeros depending on magnitude
    for idx in idxs_to_contaminate:
        if isinstance(data, pd.DataFrame):
            data.iloc[idx] *= 10 ** (magnitudes[list(data.columns)[idx[1]]] + 2)
        elif isinstance(data, pd.Series):
            data.iloc[idx] *= 10 ** (magnitudes + 2)

    return data


""" Functions to contaminate any column """


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
    data: pd.DataFrame or pd.Series
        contaminated dataset
    """
    data = clean_data.copy()

    # Find random data cells to contaminate
    nan_idxs = get_random_indices(
        data, col_type="any", corruption_level=corruption_level
    )

    # Insert missing values
    for idx in nan_idxs:
        # Replace datapoint with NaN or ?
        nan_val = np.random.choice(["?", np.nan], p=[0.1, 0.9])
        if isinstance(data, pd.DataFrame):
            data.iloc[idx] = nan_val
        else:
            data[idx] = nan_val

    return data


""" Functions for duplications: """


def duplicate_rows(data, corruption_level=4):
    """
    Add extra rows in a dataset

    Parameters
    ----------
    data: pd.DataFrame
        dataset to be contaminated
    corruption_level: int, optional
        level of corruption, should be between 0 and 10, where 0 leaves the dataset as is, 10
        is the highest level of contamination

    Returns
    -------
    data: pd.DataFrame
        data with duplicated rows
    """
    n_rows, _ = data.shape
    n_rows_duplicated = int(np.ceil(n_rows * (0.2 * corruption_level / 10)))

    dupes = data.sample(n=n_rows_duplicated, axis=0)
    data = pd.concat([data, dupes], axis=0, ignore_index=True)

    return data


def duplicate_columns(data, corruption_level=4):
    """
    Add extra columns in a dataset

    Parameters
    ----------
    data: pd.DataFrame
        dataset to be contaminated
    corruption_level: int, optional
        level of corruption, should be between 0 and 10, where 0 leaves the dataset as is, 10
        is the highest level of contamination

    Returns
    -------
    data: pd.DataFrame
        data with duplicated columns
    """
    _, n_cols = data.shape
    n_cols_duplicated = int(np.ceil(n_cols * (0.2 * corruption_level / 10)))

    dupes = data.sample(n=n_cols_duplicated, axis=1)
    data = pd.concat([data, dupes], axis=1, ignore_index=True)

    return data
