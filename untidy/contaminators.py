import pandas as pd

""" Functions to contaminate the data """

""" Column-wise contaminators """

""" Functions to contaminate any columns: """


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


""" Functions for duplications: """


def duplicate_rows(data, corruption_level=4):
    """
    Contaminate an array with extra characters.

    Parameters
    ----------
    data: pd.DataFrame
        dataset to be contaminated
    corruption_level: int, optional
        level of corruption, should be between 0 and 10, where 0 leaves the dataset as is, 10
        is the highest level of contamination

    Returns
    -------
    Dataset with duplication
    """
    n_rows, _ = data.shape
    n_rows_duplicated = int(n_rows * corruption_level / 10)

    selected_df = data.sample(n=n_rows_duplicated, axis=0, replace=False, weights=None)

    return pd.concat([data, selected_df], axis=0, ignore_index=True)


def duplicate_columns(data, corruption_level=4):
    """
    Contaminate an array with extra characters.

    Parameters
    ----------
    data: pd.DataFrame
        dataset to be contaminated
    corruption_level: int, optional
        level of corruption, should be between 0 and 10, where 0 leaves the dataset as is, 10
        is the highest level of contamination

    Returns
    -------
    Dataset with duplication
    """
    _, n_cols = data.shape
    n_cols_duplicated = int(n_cols * corruption_level / 10)

    selected_df = data.sample(n=n_cols_duplicated, axis=1, replace=False, weights=None)

    return pd.concat([data, selected_df], axis=1, ignore_index=True)
