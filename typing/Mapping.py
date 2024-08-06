from typing import Mapping, Dict

'''
Dict、字典，是 dict 的泛型；Mapping，映射，是 collections.abc.Mapping 的泛型。
根据官方文档，Dict 推荐用于注解返回类型，Mapping 推荐用于注解参数。
它们的使用方法都是一样的，其后跟一个中括号，中括号内分别声明键名、键值的类型
'''
def size(rect: Mapping[str, int]) -> Dict[str, int]:
    return {'width': rect['width'] + 100, 'height': rect['width'] + 100}

'''
这里将 Dict 用作了返回值类型注解，将 Mapping 用作了参数类型注解。
MutableMapping 则是 Mapping 对象的子类，在很多库中也经常用 MutableMapping 来代替 Mapping。
'''