#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Print data from a csv to a table in the output

Example:
    python print_csv.py

Attributes:
    csv_file (string): csv to print

Todo:
    * Add argparse for arguments

@Author: mmir01
@Date: 05/05/2022

"""

import pandas as pd
import sys


if __name__ == "__main__":
    csv_file = sys.argv[1]
    df = pd.read_csv(csv_file)
    pd.options.display.max_columns = len(df.columns)
    print(df)