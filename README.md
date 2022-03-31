# Untidy
A Python library for uncleaning your dataset.

## Overview
Mess up your dataset just how you like it. A handy tool to use when your data is too clean. 

Jokes aside, the package can be applied for training purposes, to practice data cleaning. 

```
messy_df = untidy(clean_df, 
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
Can be installed via pip by downloading the `untidy-0-0-1.dev1.tar.gz` (or any other available release) file under release section. Run the command

```commandline
pip install untidy-0-0-1.dev1.tar.gz
```
 
* * *

<p align="center">
  <img src="https://github.com/dainstudios/untidy/blob/main/resources/dain-logo.svg" alt="DAIN logo" width="250"/>
</p>
