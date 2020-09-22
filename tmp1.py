#!/usr/bin/python3 

import sys 

try: 
    a =4/0
except ZeroDivisionError as e: 
    print("error")
    sys.exit(1)
    print('exited')
finally: 
    print('finally')