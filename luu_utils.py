# -*- coding: utf-8 -*-
"""
Description: 
    
Created on %(date)s

@author: %(username)s

Contact: tpluu2207 at gmail.com
"""
# =============================================================================
# IMPORT PACKAGES
import os, inspect, datetime
# =============================================================================
# SETTINGS and GLOBAL VARIABLES

# =============================================================================
def get_varargin(kwargs, inputkey, defaultValue):
    outputVal = defaultValue
    for key, value in kwargs.items():
        if key == inputkey:
            outputVal = value
        else:
            pass
    return outputVal
# =============================================================================
def todaystr():
    todaystr = datetime.datetime.today().strftime('%Y-%m-%d')
    return todaystr
# =============================================================================

    
# =============================================================================
# Example class
class exampleclass(object):
    # Initialize
    def __init__ (self, arg1):
        self.arg1 = arg1
    def func1(self):  
        pass
        
# =============================================================================
# Example functions
# Function with keyworded argument
def greet_me(**kwargs):
    print('RUNNING: %s' % inspect.stack()[0][3])
    # ==== BEGIN ====
    for key, value in kwargs.items():
        print("{0} = {1}".format(key, value))
    
    print('DONE: %s' % inspect.stack()[0][3])
    # ==== END ====

# Functions with optional arguments
def test_var_args(f_arg, *argv):
    print("first normal arg:", f_arg)
    for arg in argv:
        print("another arg through *argv:", arg)        
    
# =============================================================================
# MAIN
def main():
    pass
# =============================================================================
# DEBUG
if __name__ == '__main__':
    main()