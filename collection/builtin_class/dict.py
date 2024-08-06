# 动态继承
# @web: https://blog.csdn.net/qq_24487005/article/details/123820562
from collections import OrderedDict
from pprint import *
# OrderedDict inherit dict

def create_dict(cls):
    class DD(cls):
        def __init__(self, *args, **kwargs):
            super(type(self), self).__init__(*args, **kwargs)
            if args:
                for arg in args:
                    for key, value in arg.items():
                        # if isinstance(value, dict):
                        #     self[key] = type(self)(value)
                        # if (isinstance(value, dict) and isinstance(self, OrderedDict)) or \
                        #     (isinstance(value, OrderedDict) and isinstance(self, dict)):
                        #     print(self.__class__.__bases__[0].__bases__[0])
                        #     print(value.__class__)
                        #     self[key] = type(self)(value)
                        if self.__class__.__bases__[0].__bases__[0] == value.__class__ or \
                            self.__class__.__bases__[0] == value.__class__.__bases__[0]:
                            self[key] = type(self)(value)

        # ((d[12]) [23] = "test")
        # getitem
        #       setitem
        def __getitem__(self, key):
            # such as: sub_d = d[12]
            if key in self:
                return super().__getitem__(key)
            # return self.setdefault(key, DD())
            return self.setdefault(key, type(self)())

        def __setitem__(self, key, value):
            if key in self:
                print(f">before: {self[key]}")
                print(f">set:    {value}")
            super().__setitem__(key, value)

        def merge(self, dic, inplace=False):
            res = type(self)({**self, **dic})
            if not inplace:
                return res
            self.update(res)
            return self
    return DD

if __name__ == "__main__":
    # d = DD()
    d = create_dict(dict)
    print(d)
    d = d()
    d = create_dict(OrderedDict)()
    print(d)
    d[12][23] = "test"
    d[12]["demo"] = 1
    print(d[12][23])
    sub_d = d[12]
    print(sub_d)
    d[12] = "dei"
    print(d[12])

    print("######### merge ##########")
    d2 = create_dict(OrderedDict)({12: 1, 100: 100})
    d3 = d.merge(d2, inplace=True)
    print(d)
    print(d3)

    print("######### __init__ ##########")
    dd = create_dict(OrderedDict)({12: 1, "test": {100: 100}})
    print(dd)
    dd = create_dict(dict)({12: 1, "test": {100: 100}})
    print(dd)