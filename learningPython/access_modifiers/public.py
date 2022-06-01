#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
How private works in python.
First example > PUBLIC

@Author: mmir01
@Date: 23/05/2022
"""

class Company:
    # Class atrributes
    # These attributes are public and can be accessed outside the class environment
    companyName = "My Company LTD"
    country = "United Kingdom"
    
    def __init__(self, location):
        # instance attribute
        self.office = location
    
    def printData(self):
        print ("Data of your company:")
        print(self.companyName)
        print("Office: " + self.office)
        print("Country: " + self.country)
    
        
def printHello():
    #Public method outside a class
    print "Hello"
    
    
if __name__ == "__main__":
    
    ## PUBLIC ATTRIBUTES
    
    # Class attributes are accessible even if we don't have an instance
    print("Public attributes: " + Company.companyName + " - " + Company.country)
    
    # This will print an error as office attribute is only created when an instance in initialized
    #print("Office: " + Company.office)
    # It will print: 
    # AttributeError: class Company has no attribute 'office'
    
    
    # Creating an instance of the class
    myCompany = Company("London")
    
    # All attributes are accesible
    print("Office: " + myCompany.office)
    
    
    ## PUBLIC METHODS
    
    # We can call "printHello" method without using an instance, as it is defined
    # outside a class
    printHello()
    
    # To use the public methods defined inside the class, we need an instance
    #Company.printData()
    # It will fail:
    # TypeError: unbound method printData() must be called with Company instance as first argument (got nothing instead)
    #Using an instance
    myCompany.printData()
