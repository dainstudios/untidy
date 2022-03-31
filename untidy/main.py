from untidy.contaminators import *


def _user_log(statement, verbose):
    if verbose:
        print(statement)


def untidyfy(
    clean_data,
    corruption_level=4,
    nans=True,
    outliers=True,
    text_noise=True,
    mess_with_numbers=True,
    mess_with_string_encodings=True,
    duplicate_rows=True,
    duplicate_columns=True,
    verbose=True,
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
    verbose: boolean, optional

    Examples
    -------
    >>> messy_df = untidyfy(clean_df, corruption_level=7, nans=False)

    Returns
    -------
    data: pd.DataFrame
        contaminated dataset
    """
    _user_log("Your dataset is being messed up...", verbose)
    data = clean_data.copy()

    # Contaminate
    if outliers:
        _user_log("\tAdding outliers...", verbose)
        data = add_outliers(data, corruption_level=corruption_level)
    if text_noise:
        _user_log("\tAdding noise...", verbose)
        data = add_noise_to_strings(data, corruption_level)
    if mess_with_string_encodings:
        _user_log("\tMessing with strings...", verbose)
        data = change_str_encoding(data, corruption_level)
    if mess_with_numbers:
        _user_log("\tMessing with numbers....", verbose)
        data = change_numeric_to_str(data, corruption_level)
    if nans:
        _user_log("\tAdding missing values...", verbose)
        data = add_nans(data, corruption_level=corruption_level)
    if duplicate_rows:
        _user_log("\tAdding duplicate rows...", verbose)
        data = add_duplicate_rows(data, corruption_level=corruption_level)
    if duplicate_columns:
        _user_log("\tAdding duplicate columns...", verbose)
        data = add_duplicate_columns(data, corruption_level=corruption_level)

    _user_log("\nYour untidy dataset is ready.", verbose)

    return data
