# Untidy
A Python library for uncleaning your dataset.

[![Check
status](https://github.com/dainstudios/untidy/actions/workflows/check.yml/badge.svg)](https://github.com/dainstudios/untidy/actions/workflows/check.yml)

## Overview
Have you ever wondered how to introduce specific problems to your clean data? Now you can apply our out-of-the-box solution to untidy your data according to your needs.

The solution can be used primarily for educational purposes, where clean example data is made more realistic.

Real world data is often poised with missing values, datetime issues, data type mismatches, string encoding problems.

You can introduce the following problems to your data:
* Adding missing values
* Adding outliers
* Changing the encoding of strings
* Changing the data type of numeric columns to strings
* Adding duplicate rows
* Adding duplicate columns
* Adding extra characters to strings

The package is designed to work with `pandas` DataFrames.

```
from untidy import untidyfy
messy_df = untidyfy(clean_df, 
                    corruption_level=4, # how much mess you want (0-10)
                    nans=True,
                    outliers=True,
                    text_noise=True,
                    mess_with_numbers=True,
                    mess_with_string_encodings=True,
                    duplicate_rows=True,
                    duplicate_columns=True)
```

## Installation
Can be installed via directly via pip or by downloading the `untidy-{release-version}.tar.gz` file under release section. Run the command

```commandline
pip install `untidy-{release-version}.tar.gz`
```

## Contact

Mate Varadi (mate.varadi \[at] dainstudios.com)

Developed with :heart: at [DAIN Studios](https://dainstudios.com/)


## Licence
MIT License

Copyright (c) 2022 DAIN Group Oy. Helsinki, Finland.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


* * *

<p align="center">
  <img src="https://github.com/dainstudios/untidy/blob/main/resources/dain-logo.svg" alt="DAIN logo" width="250"/>
</p>
