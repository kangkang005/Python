from dataclasses import dataclass, field
from typing import List

# 复合初始化

# @web: https://www.cnblogs.com/apocelipes/p/10284346.html
# @web: https://zhuanlan.zhihu.com/p/59658598

# 被 @dataclass 装饰的类的属性又叫做字段（field）。
"""
default 和 default_factory 参数将会影响默认值的产生，它们的默认值都是 None，
意思是调用时如果为指定则产生一个为 None 的值。其中 default 是 field 的默认值，
而 default_factory 控制如何产生值，它接收一个无参数或者全是默认参数的 callable 对象，
然后用调用这个对象获得 field 的初始值，之后再将 default（如果值不是 MISSING）复制给 callable 返回的这个对象。

"""

def get_default():
    return ["here", "12"]

@dataclass
class C:
    # 如果要设置某一个字段的默认值为可变类型（例如列表、字典等），那么所有实例将共享这同一个默认值对象。
    # 这可能会导致意想不到的行为，因为修改任何一个实例的字段将影响所有实例。
    # @ERROR: ValueError: mutable default <class 'list'> for field my_list is not allowed: use default_factory
    # my_list: List[int] = []

    # 使用 default_factory 时，我们需要为它赋值一个无参数的可调用对象。每次创建数据类的实例时，
    # 都会调用这个可调用对象来生成该字段的默认值。面对以上报错，我们可以使用 default_factory 来解决
    my_list    : List[int] = field(default_factory=list)    # 默认值是空列表
    other_list : List[int] = field(default_factory=lambda: [1, 2, 3])    # 默认值是[1, 2, 3]
    his_list   : List[str] = field(default_factory=get_default)    # 默认值是[1, 2, 3]

if __name__ == "__main__":
    c1 = C()
    print(c1)
    c1.my_list += [1,2,3]
    print(c1.my_list)