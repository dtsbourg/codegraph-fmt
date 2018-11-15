"""
This is a test module.
"""

import os

def hello_world():
    c = 3
    print("Hello World!")
    c = 4
    del c

if __name__ == '__main__':
    a = 2
    hello_world()
    del a
