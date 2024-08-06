# @web: https://segmentfault.com/a/1190000007255412
# @web: https://www.cnblogs.com/yjt1993/p/11103368.html
# @web: https://www.pythontutorial.net/python-oop/python-metaclass/
from pprint import *

#定义ItemMetaClass，继承type
class ItemMetaClass(type):
    # cls 代表动态修改的类
    # name 代表动态修改的类名
    # bases 代表被动态修改的类的所有父类
    # attrs 代表被动态修改的类的所有属性、方法组成的字典

    def __new__(cls, name, bases, attrs):
        #动态为该类添加一个cal_price方法
        attrs['cal_price'] = lambda self:self.price * self._discount
        pprint(attrs)
        return type.__new__(cls, name, bases, attrs)

# type也是一个类，我们可以继承它.
class UpperAttrMetaclass(type):
    # __new__ 是在__init__之前被调用的特殊方法
    # __new__是用来创建对象并返回这个对象
    # 而__init__只是将传入的参数初始化给对象
    # 实际中,你很少会用到__new__，除非你希望能够控制对象的创建
    # 在这里，类是我们要创建的对象，我们希望能够自定义它，所以我们改写了__new__
    # 如果你希望的话，你也可以在__init__中做些事情
    # 还有一些高级的用法会涉及到改写__call__，但这里我们就先不这样.

    def __new__(upperattr_metaclass, future_class_name,
                future_class_parents, future_class_attr):

        uppercase_attr = {}
        for name, val in future_class_attr.items():
            if not name.startswith('__'):
                uppercase_attr[name.upper()] = val
            else:
                uppercase_attr[name] = val
        pprint(uppercase_attr)
        return type(future_class_name, future_class_parents, uppercase_attr)

#定义book类
class Book(metaclass=ItemMetaClass):
    __slots__ = ('name', 'price', '_discount')
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, discount):
        self._discount = discount

#定义cellPhone类
class CellPhone(metaclass=UpperAttrMetaclass):
    __slots__ = ('price', '_discount')
    def __init__(self, price):
        self.price = price

    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, discount):
        self._discount = discount

###########################################################
class Human(type):
    def __new__(mcs, name, bases, class_dict, **kwargs):
        class_ = super().__new__(mcs, name, bases, class_dict)
        if kwargs:
            for name, value in kwargs.items():
                setattr(class_, name, value)
        return class_

class Person(object, metaclass=Human, freedom=True, country='USA'):
    def __init__(self, name, age):
        self.name = name
        self.age = age

###########################################################
class MetaOne(type):
    def __new__(cls, name, bases, dict):
        print()
        print(name)
        print(bases)
        print(dict)
        print()
        return super(MetaOne,cls).__new__(cls, name, bases, dict)

class Parent():
    pass

class Child(Parent, metaclass=MetaOne):
    def __init__(self):
        pass

if __name__ == "__main__":
    #Book类实例化
    b = Book('Python基础教程', 89)
    b.discount = 0.8
    #Book类的cal_price()方法
    print(b.cal_price())

    #CellPhone类实例化
    cp = CellPhone(2300)
    cp.DISCOUNT = 0.85
    #CellPhone类的cel_price方法
    print(cp.DISCOUNT)

    pprint(Person.__dict__)

    print(Child())