# Untidy
A Python library for uncleaning your dataset.

## Overview
Mess up your dataset just how you like it. A handy tool to use when your data is too clean. 

Jokes aside, the package can be applied for training purposes, to practice data cleaning. 

```
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
Can be installed via pip by downloading the `untidy-{release-version}.tar` file under release section. Run the command

```commandline
pip install `untidy-{release-version}.tar`
```
 
* * *

<p align="center">
  <img src="https://github.com/dainstudios/untidy/blob/main/resources/dain-logo.svg" alt="DAIN logo" width="250"/>
</p>
