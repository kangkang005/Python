# @web: https://blog.csdn.net/qdPython/article/details/136157388
# order: metaclass __new__ > metaclass __init__ > metaclass __call__
#       > instance __new__ > instance __init__ > instance __call__
class MyType(type): # 自定义一个type的派生类
    def __new__(meta, name, bases, attrs):
        print('metaclass __new__')
        # 动态添加属性
        attrs['name'] = "wei"   # class.name overwrite metaclass.name
        attrs['talk'] = lambda self: print("hello")
        return super(MyType, meta).__new__(meta, name, bases, attrs)

    def __init__(self, name, bases, attrs, **kwargs):
        print('metaclass __init__')
        super(MyType, self).__init__(name, bases, attrs)

    # 元类__call__影响的是创建类的实例对象的行为，此时如果类自定义了__new__和__init__就可以控制类的对象实例的创建和初始化
    def __call__(cls, *args, **kwargs):
        print("metaclass __call__")
        obj = cls.__new__(cls,*args, **kwargs)
        cls.__init__(obj,*args, **kwargs)
        return obj

class Foo(metaclass=MyType): # metaclass=MyType,即指定了由MyType创建Foo类，当程序运行，用到class Foo时，即调用MyType的__init__方法，创建Foo类
    def __new__(cls, *args, **kwargs):
        print('instance __new__')
        return object.__new__(cls)

    def __init__(self,name):
        print('instance __init__')
        self.name = name

    def __call__(self):
        print("instance __call__")

# like: Foo.__call__("name")
a = Foo('name') # 类()，即执行元类的__call__
# like: a.__call__()
a()             # 对象()，即执行Foo的__call__
print(a.name)
a.talk()