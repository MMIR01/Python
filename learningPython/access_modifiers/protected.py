#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
How private works in python.
Second example > PROTECTED

@Author: mmir01
@Date: 23/05/2022
"""


class Company:
    # Class atrributes
    # This attribute is public and can be accessed outside the class
    # environment
    companyName = "My Company LTD"

    # This attribute is protected
    # The single underscore is just a naming convention that tells developers
    # to not directly access or modify those specific class attributes
    _country = "United Kingdom"

    def __init__(self, location):
        # instance attribute
        self.office = location

    # Protected method
    # Using a single _ to indicate the name of a private method in a Python 
    # class, it is just a naming convention and it's not enforced by the Python 
    # interpreter
    def _getCountry(self):
        return self._country

    # Public method
    def printData(self):
        print(f"Data of your company: {self.companyName}")
        print("Office: " + self.office)
        # Call protected method
        print("Country: " + self._getCountry())


if __name__ == "__main__":

    # ATTRIBUTES

    # Class attributes are accessible even if we don't have an instance
    print("Public attributes: " + Company.companyName)

    # Protected attributes shouldn't be used outside of the class
    # but Python don't use any protecction to avoid it
    print("Protected attributes: " + Company._country)

    # Creating an instance of the class
    myCompany = Company("Manchester")

    # All attributes are accesible
    print("Office: " + myCompany.office)
    print("Country: " + myCompany._country)

    # METHODS
    # We have access to the protected methods
    print("Access to the protected method: " + myCompany._getCountry())
