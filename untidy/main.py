from contaminators import *


def untidy(
    clean_data,
    corruption_level=4,
    nans=True,
    outliers=True,
    text_noise=True,
    mess_with_numbers=True,
    mess_with_string_encodings=True,
    duplicate_rows=True,
    duplicate_columns=True,
):
    """
    Contaminate a dataset with various types of data issues.

    Parameters
    ----------
    clean_data: pd.DataFrame
        dataset to be corrupted
    corruption_level: int, optional
        level of corruption, should be between 0 and 10, where 0 leaves the dataset as is, 10
        is the highest level of contamination.  Defaults to 4.
    nans: boolean, optional
        Whether to contaminate the data with NaN values (np.nan or '?').  Defaults to True.
    outliers: boolean, optional
        Whether to add outliers to the data (trailing zeros).  Defaults to True.
    text_noise: boolean, optional
        Whether to add superfluous characters to some text cells of the data.  Defaults to True.
    mess_with_numbers: boolean, optional
        Whether to change the data type of some numeric columns to string.  Defaults to True.
    mess_with_string_encodings: boolean, optional
        Whether to change the string encoding of some columns (to utf-16 or ascii).  Defaults to True.
    duplicate_rows: boolean, optional
        Whether to duplicate some rows of the data. Defaults to True.
    duplicate_columns: boolean, optional
        Whether to duplicate some columns of the data. Defaults to True.

    Examples
    -------
    >>> messy_df = untidy(clean_df, corruption_level=7, nans=False)

    Returns
    -------
    data: pd.DataFrame
        contaminated dataset
    """
    data = clean_data.copy()

    # Contaminate
    if outliers:
        data = add_outliers(data, corruption_level=corruption_level)
    if text_noise:
        data = add_noise_to_strings(data, corruption_level)
    if mess_with_string_encodings:
        data = change_str_encoding(data, corruption_level)
    if mess_with_numbers:
        data = change_numeric_to_str(data, corruption_level)
    if nans:
        data = add_nans(data, corruption_level=corruption_level)
    if duplicate_rows:
        data = add_duplicate_rows(data, corruption_level=corruption_level)
    if duplicate_columns:
        data = add_duplicate_columns(data, corruption_level=corruption_level)

    return data
