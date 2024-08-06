# 用于控制属性读写的魔术方法
# __getattr__: 拦截通过 obj.key 获取对象不存在的 key 属性时调用的方法，注意与__getattribute__方法的区别，可实现懒加载，在调用属性时再去操作耗时的动作，如文件读取等。
# __getattribute__：拦截所有的属性访问，注意避免在此方法中使用 self.key，以免造成死循环
# __setattr__: 拦截所有属性的赋值操作，注意避免在此方法中通过 self.key=value 的方式给实例赋值，以免造成死循环。
# __delattr__: 拦截所有属性的清除操作，注意避免在此方法中通过 del self.key 的方式清除实例属性，以免造成死循环。
class World:
    def __init__(self, countries):
        self.countries = countries

    # `self.name # name不存在` 访问一个不存在的属性时
    def __getattr__(self, key):
        print(f"__getattr__ called: unexisted key {key}")
        return None

    # `self.name` 访问任何属性时
    def __getattribute__(self, key):
        print(f"__getattribute__ called: key {key}")
        return super(World, self).__getattribute__(key)

    # `self.name = val` 对一个属性赋值时
    def __setattr__(self, key, value):
        if key in self.__dict__:
            print(f"__setattr__ called: key existed {key}")
        else:
            print(f"__setattr__ called: key unexisted {key}")
        self.__dict__[key] = value

    # `del self.name` 删除一个属性时
    def __delattr__(self, key):
        print(f"__delattr__ called: key {key}")
        del self.__dict__[key]

w = World(256)
print(w.oceans)
w.oceans = 5
del w.countries
"""
Output:
# __getattribute__ called: key __dict__
#__setattr__ called: key unexisted countries
# __getattribute__ called: key __dict__

# __getattribute__ called: key oceans
# __getattr__ called: unexisted key oceans
# None

# __getattribute__ called: key __dict__
# __setattr__ called: key unexisted oceans
# __getattribute__ called: key __dict__

# __delattr__ called: key countries
# __getattribute__ called: key __dict__
"""