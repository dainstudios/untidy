""" Functions to contaminate the data """
import pandas as pd
import numpy as np
import random

""" Helpers """


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

    if isinstance(data, pd.DataFrame):
        # Find columns to sample from
        if col_type == "any":
            cols_to_sample = range(len(data.columns))
        elif col_type.startswith("str"):
            cols_to_sample = [
                list(data.columns).index(col)
                for col in data.select_dtypes(include=["object", "category"]).columns
            ]
        elif col_type.startswith("num"):
            cols_to_sample = [
                list(data.columns).index(col)
                for col in data.select_dtypes(include=["float64", "int64"]).columns
            ]
        cols_to_sample = list(cols_to_sample)
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
    noise_chars = "%&$?!#"
    whitespace = "  "

    for idx in idxs_to_contaminate:
        # add either extra whitespace or a superfluous character
        noise_char = random.choice(noise_chars)
        noise = random.choice([noise_char, whitespace])
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
        numeric_cols = list(data.select_dtypes(include=["float64", "int64"]).columns)
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
    contaminated data as pd.DataFrame or pd.Series
    """
    data = clean_data.copy()

    # Find random data cells to contaminate
    nan_idxs = get_random_indices(
        data, col_type="any", corruption_level=corruption_level
    )

    # Insert missing values
    for x, y in nan_idxs:
        if isinstance(data, pd.DataFrame):
            data.iloc[x, y] = np.nan
        else:
            data[x] = np.nan

    return data
