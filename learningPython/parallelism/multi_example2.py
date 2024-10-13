#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
How to run various processes simultaneously in python by using multiprocessing
library.
In this example we are going to run 2 sets of processes

Example:
    python multi_example2.py
Attributes:
    N/A
Todo:
    * N/A

@Author: mmir01
@Date: 10/08/2022
"""

import multiprocessing
import time


def function1(**kwargs):
    arg1 = kwargs.get('arg1', None)

    print("Running function1: arg1: %s" % (arg1))
    time.sleep(2)
    print("End function1")


def setrun(**kwargs):
    args_list = kwargs.get('args_list', None)

    procs = []

    for a in args_list:
        param = {"arg1": a}
        process1 = multiprocessing.Process(target=function1, kwargs=(param))
        procs.append(process1)

    for proc in procs:
        proc.start()
        #print("Alive: %s" % proc.is_alive())

    for proc in procs:
        proc.join()


if __name__ == "__main__":

    list1 = ["a1", "a2", "a3"]
    setrun(args_list=list1)

    list2 = ["b1", "b2", "b3"]
    setrun(args_list=list2)
