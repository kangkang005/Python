# 反射，实例类型判断
# __instancecheck__: 支持 instancecheck 方法
# __subclasscheck__: 支持 subclasscheck 方法，此两个方法需定义在元类中，否则调用的还是 type 中的方法 4
class MyType(type):
    def __instancecheck__(self, instance):
        print("__instancecheck__ called")
        if hasattr(instance, "password"):
            return True
        # 否则返回False
        return False


class A(metaclass=MyType):
    def __init__(self, x):
        super(A, self).__init__()
        self.x = x

a = []
print(isinstance(a, A))

class MyType(type):

    def __subclasscheck__(self, subclass):
        print("__subclasscheck__ called.")
        return hasattr(subclass, "password")

class B(metaclass=MyType):
    pass

b = B()
print(issubclass(b, B))
b = B()
b.password = "12"
print(issubclass(b, B))