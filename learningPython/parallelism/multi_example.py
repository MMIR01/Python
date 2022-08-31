#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
How to run various processes simultaneously in python by using multiprocessing library

Example:
    python multi_example.py
Attributes:
    N/A
Todo:
    * N/A
    
@Author: mmir01
@Date: 01/08/2022
"""

import multiprocessing
import time

def function1():
    print("Running function 1")
    time.sleep(5)
    print("End function 1")

def function2(**kwargs):
    arg1  = kwargs.get('arg1', None)
    arg2  = kwargs.get('arg2', None)
    
    print("Running function2: %s-%s" % (arg1,arg2))
    time.sleep(2)
    print("End function2")

if __name__ == "__main__":
    
    procs = []
    
    process1 = multiprocessing.Process(target=function1)
    param = {"arg1": "a", "arg2": "b"}
    process2 = multiprocessing.Process(target=function2, kwargs=(param))
    
    procs.append(process1)
    procs.append(process2)
    
    for proc in procs:
        proc.start()

    for proc in procs:
        proc.join()
    
