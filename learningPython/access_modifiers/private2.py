#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
How private works in python.
Another example about PRIVATE

@Author: mmir01
@Date: 23/05/2022
"""

class Company:
    # Class atrributes
    # This attribute is public and can be accessed outside the class environment
    companyName = "My Company LTD"
    # These attributes are private, so it can be only accessed inside the class
    __country = "United Kingdom"
    __office = "London"
    
               
    # Public methods
    def insertData1(self, ceoName, ctoName):
        # This is not OK. We are creating variables that are temporal
        # and they are not going to exist after the method execution
        # However it can be used inside the method without any issue, 
        # but it would be the same if we don't use the double underscore
        __ceo1 = ceoName
        __cto1 = ctoName
        print("Inserting CEO and CTO via method 1:")
        print("CEO: " + __ceo1)
        print("CTO: " + __cto1)

    def insertData2(self, ceoName, ctoName):
        # This is OK. We are creating private attributes for the object
        # (class instance), so it can be used after method execution
        self.__ceo2 = ceoName
        self.__cto2 = ctoName
        print("Inserting CEO and CTO via method 2:")
        print("CEO: " + self.__ceo2)
        print("CTO: " + self.__cto2)
    
    # This method will fail
    def getData1(self):
        print ("CEO of the company:")
        print(__ceo1)
        print ("CTO of the company:")
        print(__cto1)

    # This method is OK
    def getData2(self):
        print ("CEO of the company:")
        print(self.__ceo2)
        print ("CTO of the company:")
        print(self.__cto2)
            
    def doSomething(self):
        __var1 = "Variable 1"
        var2 = "Variable 2"
        print (__var1 + " and " + var2)
    
if __name__ == "__main__":
    
    myCompany = Company()
    
    # So basically, it makes no sense to use '__' for variables inside a method 
    # as by definition a variable defined in a method is only created and exists
    # when the method is executed
    # Another example:
    myCompany.doSomething()
    # You cannot use neither __var1 or var2 (they are not attributes of the object)
    #myCompany.__var1
    #myCompany.var2
    
    # This will work, as we are using attributes of the instance
    print("Access to attributes: " + myCompany.companyName)
    
    
    ## METHODS
    myCompany.insertData1("John", "Elisabeth")
    myCompany.insertData2("Ellen", "George")
    
    
    # This one will fail as __ceo1 and __cto1 are not attributes, so they are not defined
    # when getData1 is called
    #myCompany.getData1()
    
    # This one is fine
    myCompany.getData2()
    
    
    # A note about private attributes
    # Private attributes cannot be used outside the class
    #print("Private attributes: " + Company.__country)
    # Error:
    # AttributeError: class Company has no attribute '__country'
    
    # The same with the object
    #print("Private attributes: " + myCompany.__country)
    #Error:
    #AttributeError: Company instance has no attribute '__country'
