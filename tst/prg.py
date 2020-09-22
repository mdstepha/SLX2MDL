#!/usr/bin/python3 

filepath = 'mxarrays/UserData_73.mxarray'


with open(filepath, 'rb') as file: 
    x = file.read()
    print(x)