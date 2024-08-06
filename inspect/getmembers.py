import inspect
import math
from pprint import pprint

# get all methods of math
members = inspect.getmembers(math)
pprint(members)

########################################
class MyClass:
    def method_one(self):
        pass

    def method_two(self):
        pass

# get method of class
# predicate is filter
methods = inspect.getmembers(MyClass, predicate=inspect.isfunction)
pprint(methods)