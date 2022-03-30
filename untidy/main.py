from contaminators import *


def run(clean_data, corruption_level=4):
    """
    Contaminate a dataset with various types of data issues.

    Parameters
    ----------
    data: pd.DataFrame
        dataset to be corrupted
    corruption_level: int, optional
        level of corruption, should be between 0 and 10, where 0 leaves the dataset as is, 10
        is the highest level of contamination
    """
    # Read dataset

    # Contaminate
    data = clean_data.copy()
    data = add_nans(data, corruption_level = corruption_level)
    data = add_outliers(data, corruption_level = corruption_level)

    # Save / return
