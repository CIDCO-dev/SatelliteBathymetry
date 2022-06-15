from pprint import pprint
import numpy
import importlib
import sys

module = numpy
# attributes = ['__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__']
#
#
# for attribute in attributes:
#     print(getattr(module, attribute))

for el in (dir(numpy)):
    print(el)
