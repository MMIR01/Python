#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
How to run various processes simultaneously in python by using multiprocessing
pool.
In this example we are going to run 6 processes in parallel twice,
but here the function to be parallelized uses named arguments

Example:
    python multi_pool_example2.py
Attributes:
    N/A
Todo:
    * N/A


@Author: mmir01
@Date: 11/08/2022
"""

from multiprocessing import Pool
import time


def function1(**kwargs):
    arg1 = kwargs.get('arg1', None)

    print("Connection: %d" % (arg1))
    time.sleep(1)
    print("End connection: %d" % (arg1))


# multiprocessing.pool.Pool.map doc states:
# A parallel equivalent of the map() built-in function
# (it supports only one iterable argument though).
# It blocks until the result is ready.
# So we need a wrapper
def function1_wrapper(arg):
    return function1(arg1=arg)


def setrun(**kwargs):
    num_connections = kwargs.get('num_connections', None)

    params = []
    for i in range(1, num_connections + 1):
        params.append(i)

    proc = Pool(num_connections)
    proc.map(function1_wrapper, params)


if __name__ == "__main__":

    print("First run")
    num_connections = 6
    setrun(num_connections=num_connections)

    print("Second run")
    num_connections = 6
    setrun(num_connections=num_connections)
