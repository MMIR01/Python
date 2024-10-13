#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
How to run various processes simultaneously in python by using threads

Example:
    python thread_example.py
Attributes:
    N/A
Todo:
    * N/A

Note: from testdriven.io
"A thread is a way of allowing your computer to break up a single
process/program into many lightweight pieces that execute in parallel.
Somewhat confusingly, Python's standard implementation of threading limits
threads to only being able to execute one at a time due to something called
the Global Interpreter Lock (GIL). The GIL is necessary because CPython's
(Python's default implementation) memory management is not thread-safe.
Because of this limitation, threading in Python is concurrent, but not
parallel. To get around this, Python has a separate multiprocessing module not
limited by the GIL that spins up separate processes, enabling parallel
execution of your code. Using the multiprocessing module is nearly identical
to using the threading module"

@Author: mmir01
@Date: 01/08/2022
"""

import threading
import time


def function1(arg1):
    print("Running function: %d" % (arg1))
    time.sleep(2)
    print("End function: %d" % (arg1))


def function2(**kwargs):
    arg1 = kwargs.get('arg1', None)
    arg2 = kwargs.get('arg2', None)

    print("Running function2: %s-%s" % (arg1, arg2))
    time.sleep(2)
    print("End function2: %s-%s" % (arg1, arg2))


if __name__ == "__main__":
    # Initiate empty list of threads
    threads = []

    repeat = 4
    for i in range(0, repeat):
        # Generate thread ID and run command for each page on each node in
        # parallel
        newthread = threading.Thread(target=function1, args=(i,))
        threads.append(newthread)

    param = {"arg1": "a", "arg2": "b"}
    newthread = threading.Thread(target=function2, kwargs=(param))
    threads.append(newthread)

    # Start threads
    for thread in threads:
        thread.start()

    # Wait for threads to finish
    for thread in threads:
        thread.join()
