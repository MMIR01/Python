#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
How to run various processes simultaneously in python by using multiprocessing.
In this example, we are going to return data by using pipes

Example:
    python multi_example3_return.py
Attributes:
    N/A
Todo:
    * N/A

@Author: mmir01
@Date: 22/08/2022
"""

import multiprocessing


def function1(**kwargs):
    arg1         = kwargs.get('arg1', None)
    arg2         = kwargs.get('arg2', None)
    process_pipe = kwargs.get('process_pipe', None)

    message = str(arg1) + " * " + str(arg2)
    # Return a tuple with a message plus an integer
    process_pipe.send([message, arg1*arg2])
    process_pipe.close()


def setrun(**kwargs):
    args_list = kwargs.get('args_list', None)

    # Create a pipe to receive data (result_code, failed_ops) from the child
    # process
    parent_conn, child_conn = multiprocessing.Pipe()
    param = {"arg1": args_list[0],
             "arg2": args_list[1],
             "process_pipe": child_conn}

    proc = multiprocessing.Process(target=function1, kwargs=(param))

    proc.start()
    operation, result = parent_conn.recv()
    proc.join()

    print("Operation: %s" % operation)
    print("Result: %d" % result)


if __name__ == "__main__":
    list1 = [1, 3]
    setrun(args_list=list1)

    list2 = [2, 4]
    setrun(args_list=list2)
