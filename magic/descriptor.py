# 描述器
# 描述器让对象能够自定义属性查找、存储和删除的操作。描述器是任何一个定义了 __get__()，__set__() 或__delete__() 的对象。描述器的主要目的是提供一个挂 钩，允许存储在类变量中的对象控制在属性查找期间发生的情况。5。 类似于 Java 类中的 getters\setters6。常用于动态查找，属性托管，定制名称，自定义验证等。
# __get__: 查找属性时调用
# __set__: 给属性赋值时调用
# __delete__: 移除属性时调用
import logging
logging.basicConfig(level=logging.INFO)
class LoggedAgeAccess:
    def __get__(self, obj, objtype=None):
        value = obj._age
        logging.info('Accessing %r giving %r', 'age', value)
        return value
    def __set__(self, obj, value):
        logging.info('Updating %r to %r', 'age', value)
        obj._age = value

class Person:
    age = LoggedAgeAccess() # Descriptor instance
    def __init__(self, name, age):
        self.name = name
        self.age = age
                            # Regular instance attribute # Calls __set__()__set__()
    def birthday(self):
        self.age += 1