from typing import Type

class MyClass:
    def __init__(self):
        print("create MyClass")

def my_function(cls: Type[MyClass]) -> MyClass:
    return cls()

obj: MyClass = MyClass()
obj1: MyClass = my_function(MyClass)