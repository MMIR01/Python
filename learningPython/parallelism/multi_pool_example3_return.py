#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
How to run various processes simultaneously in python by using multiprocessing
pool.
In this example we are to get returned value for each process

Example:
    python multi_pool_example3_return.py
Attributes:
    N/A
Todo:
    * N/A

@Author: mmir01
@Date: 19/08/2022
@Python Version: 3.10
"""

from multiprocessing import Pool


def function1(num, val):
    print("Connection: %d" % (num))
    to_return = ("Value1: %d" % num, "Value2: %d" % val)
    return to_return


def setrun(**kwargs):
    num_connections = kwargs.get('num_connections', None)

    params = []
    for i in range(1, num_connections + 1):
        # Append: tuple inside a list
        # In this case: (i, i*i)
        params.append((i, i*i))

    proc = Pool(num_connections)
    # Starmap instead of map in order to pass more than 1 argument
    values_returned = proc.starmap(function1, params)

    for val in values_returned:
        print(val)


if __name__ == "__main__":

    print("First run")
    num_connections = 6
    setrun(num_connections=num_connections)

    print("Second run")
    num_connections = 3
    setrun(num_connections=num_connections)
