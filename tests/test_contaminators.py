import pandas as pd
import numpy as np

from untidy.contaminators import (
    get_random_cols,
    get_random_indices,
    add_noise_to_strings,
    change_str_encoding,
    change_numeric_to_str,
    add_nans,
    add_duplicate_rows,
    add_outliers,
    add_duplicate_columns,
)

data = pd.DataFrame(
    {
        "num1": list(np.linspace(0, 20, 21)),
        "num2": list(range(21)),
        "str1": [str(n) for n in range(21)],
        "str2": [str(n) for n in list(np.linspace(0, 20, 21))],
    }
)


def test_get_random_cols():

    str_idx = get_random_cols(data, "str", return_index=True)
    str_name = get_random_cols(data, "str", return_index=False)
    num_idx = get_random_cols(data, "num", return_index=True)
    num_name = get_random_cols(data, "num", return_index=False)

    # check outputs are correct
    assert str_idx in [[2], [3]], f"got {str_idx} instead of [2] or [3]"
    assert str_name in [
        ["str1"],
        ["str2"],
    ], f"got {str_name} instead of ['str1'] or ['str2']"
    assert num_idx in [[0], [1]], f"got {num_idx} instead of [0] or [1]"
    assert num_name in [
        ["num1"],
        ["num2"],
    ], f"got {num_name} instead of ['num1'] or ['num2']"


def test_get_random_indices():

    # check string columns
    str_col = get_random_indices(data, col_type="str", corruption_level=4)

    for row_idx, col_idx in str_col:
        # check output ranges
        assert row_idx < len(
            data.index
        ), f"data has size {data.shape[0]}, row index {row_idx} out of range"
        assert col_idx < len(
            data.columns
        ), f"data has size {data.shape[1]}, row index {col_idx} out of range"
        # check output indices type
        assert data.iloc[:, col_idx].dtypes in [
            "object"
        ], f"column {data.columns[col_idx]} is not str"

        # check numeric columns
    num_col = get_random_indices(data, col_type="num", corruption_level=4)

    for row_idx, col_idx in num_col:
        assert row_idx < len(
            data.index
        ), f"data has size {data.shape[0]}, row index {row_idx} out of range"
        assert col_idx < len(
            data.columns
        ), f"data has size {data.shape[1]}, row index {col_idx} out of range"
        assert data.iloc[:, col_idx].dtypes in [
            "float64",
            "int64",
        ], f"data {data.columns[col_idx]} is not numeric"


""" Functions to contaminate text columns """


def test_add_noise_to_strings():
    noisy_strings = add_noise_to_strings(data)

    # check that numeric columns are untouched
    assert data.select_dtypes(include=["float64", "int64"]).equals(
        noisy_strings.select_dtypes(include=["float64", "int64"])
    ), "numeric columns should stay the same"
    # check that string columns are different
    assert not data.select_dtypes(include="object").equals(
        noisy_strings.select_dtypes(include="object")
    ), "string columns should be different"

    # Check that removing noise characters reverts the function
    for col in noisy_strings.select_dtypes(include="object").columns:
        for char in "%&$?!# ":
            noisy_strings[col] = noisy_strings[col].map(lambda x: x.replace(char, ""))

    assert noisy_strings.equals(data), "check remaining noise characters"


def test_change_str_encoding():
    encoded_str = change_str_encoding(data)

    assert isinstance(encoded_str.str1[0], bytes) or isinstance(
        encoded_str.str2[0], bytes
    )


""" Functions to contaminate numerical columns """


def test_change_numeric_to_str():
    data_type = change_numeric_to_str(data)

    str_cols = data.select_dtypes(include="object").columns
    num_cols = data.select_dtypes(include=["float64", "int64"]).columns

    # check str columns are untouched
    assert data_type[str_cols].equals(data[str_cols])
    # check numeric columns are different
    assert not data_type[num_cols].equals(data[num_cols])
    # check that some numeric columns are now strings
    assert (
        len(
            list(
                set(data_type[num_cols].select_dtypes(include="object").columns)
                - set(str_cols)
            )
        )
        > 0
    )


def test_add_outliers():
    outlier_df = add_outliers(data)

    # check that larger values are now in numeric columns
    assert (outlier_df["num1"] - data["num1"] > 0).any()
    assert (outlier_df["num2"] - data["num2"] > 0).any()


""" Functions to contaminate any column """


def test_add_nans():
    nan_df = add_nans(data)

    # check for missing values or '?' characters
    assert (nan_df == np.nan).any().any() or (nan_df == "?").any().any()


""" Functions for duplications: """


def test_add_duplicate_rows():
    dup_rows = add_duplicate_rows(data)

    assert dup_rows.shape[0] > data.shape[0]
    assert dup_rows.drop_duplicates().equals(data)


def test_add_duplicate_columns():
    dup_cols = add_duplicate_columns(data)
    assert dup_cols.shape[1] > data.shape[1]
