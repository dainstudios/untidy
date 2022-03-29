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
