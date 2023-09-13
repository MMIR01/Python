#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
How to run various processes simultaneously in python by using multiprocessing.
In this example, we are going to return data by using multiprocessing value

Example:
    python multi_example4_return.py
Attributes:
    N/A
Todo:
    * N/A

@Author: mmir01
@Date: 10/08/2023
"""

import multiprocessing
from random import randint

def function1(**kwargs):
    arg1         = kwargs.get('arg1', None)
    shared_value = kwargs.get('shared_value', None)
    
    # Generate random number
    myRandom = randint(100, 1000)
    shared_value.value = myRandom
    
    print("Execution number: %d" % arg1)


def setrun(**kwargs):
    totalExec  = kwargs.get('total_executions', None)
       
    procList = []
    # Create a shared value to receive data from the child process
    for i in range (1, totalExec+1):
        # i = integer
        randomNum = multiprocessing.Value('i', 0)
        
        param = {"arg1": i,
                 "shared_value": randomNum}
    
        proc = multiprocessing.Process(target=function1, kwargs=(param))
        procList.append([proc, randomNum])
    
    # Start all process (this could be done in the loop above)
    for proc, randomNum in procList:    
        proc.start()
        # Wait until the process finishes
        proc.join()
        # Print the shared value
        print("Random Number: %d" % randomNum.value)


if __name__ == "__main__":
    # 6 execution    
    setrun(total_executions=6)
