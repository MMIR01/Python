#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
How to run various processes simultaneously in python by using multiprocessing
pool.
In this example we are going to run 6 processes in parallel twice

Example:
    python multi_pool_example.py
Attributes:
    N/A
Todo:
    * N/A

@Author: mmir01
@Date: 11/08/2022
"""

from multiprocessing import Pool
import time


def function1(num):
    print("Connection: %d" % (num))
    time.sleep(1)
    print("End connection: %d" % (num))


def setrun(**kwargs):
    num_connections = kwargs.get('num_connections', None)

    params = []
    for i in range(1, num_connections + 1):
        params.append(i)

    proc = Pool(num_connections)
    proc.map(function1, params)


if __name__ == "__main__":

    print("First run")
    num_connections = 6
    setrun(num_connections=num_connections)

    print("Second run")
    num_connections = 6
    setrun(num_connections=num_connections)
