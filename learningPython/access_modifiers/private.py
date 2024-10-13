#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
How private works in python.
Third example > PRIVATE

@Author: mmir01
@Date: 23/05/2022
"""


class Company:
    # Class atrributes
    # This attribute is public and can be accessed outside the class 
    # environment
    companyName = "My Company LTD"

    # This attribute is private (double underscore)
    __country = "United Kingdom"

    def __init__(self, location):
        # instance attribute
        self.office = location

    # Private method
    def __getCountry(self):
        return self.__country

    # Public methods
    def doSomething(self):
        pass

    def printData(self):
        print("Data of your company:")
        print(self.companyName)
        print("Office: " + self.office)
        # Call protected method
        print("Country: " + self.__getCountry())


if __name__ == "__main__":

    # ATTRIBUTES
    # Class attributes are accessible even if we don't have an instance
    print("Public attributes: " + Company.companyName)

    # Private attributes cannot be used outside the class
    # print("Private attributes: " + Company.__country)
    # Error:
    # AttributeError: class Company has no attribute '__country'

    # Even with an instance of the class, we cannot access to the private
    # attribute
    myCompany = Company("Liverpool")
    #print("Country: " + myCompany.__country)
    # Error:
    # 'AttributeError: Company instance has no attribute '__country'

    # Although this is not true because there is a way to access:
    print("Accessing to private attributes: " + myCompany._Company__country)

    # METHODS
    # The same with the private method, cannot be accessed
    # print("Access to the protected method: " + myCompany.__getCountry())
    # Error:
    # AttributeError: Company instance has no attribute '__getCountry'

    # However the private method can be used inside a method from the class
    myCompany.printData()
