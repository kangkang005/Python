# 用于对象构造析构的魔术方法
# __init__: 在定义 class 时使用最多的方法，用于初始化对象，在创建对象时自动调用。
# __new__: 初始化对象时，在__init__之前调用的方法，该方法实现对象的构造，返回对象实例给__init__中的 self。
# __del__：__del__方法是定义类的析构函数，其并不是为了定义 del Object 时对象的行为，而是为了在对象被垃圾回收时执行特定的操作，如关闭 socket, 文件描述符等。因为当 Python 解释器退出时，对象有可能依然未被释放，因此__del__中定义册操作不一定能被执行，故在实际中应避免使用__del__。
class World:
    def __new__(cls, *args, **kargs):
        print("__new__ method called.")
        inst = super(World, cls).__new__(cls)
        return inst
    def __init__(self, countries):
        print("__init__ method called.")
        self.countrie = countries
    def __del__(self):
        print("Your World Is Cleaned Up.")

w = World(1)
o = World(2)
del o
"""
Output:
# __new__ method called.
# __init__ method called.
# __new__ method called.
# __init__ method called.
# Your World Is Cleaned Up.
"""