from collections.abc import Iterable

# @web: https://blog.csdn.net/weixin_43866211/article/details/101777441
# @web: https://segmentfault.com/a/1190000009781688

# Example of flattening a nested sequence using subgenerators
def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x)   # 这里递归调用，如果x是可迭代对象，继续分解
        else:
            yield x

# not use yield from
def flatten_1(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            for i in flatten_1(x):
                yield i
        else:
            yield x

items = [1, 2, [3, 4, [5, 6], 7], 8]
# Produces 1 2 3 4 5 6 7 8
for x in flatten(items):
    print(x)

print()
for x in flatten_1(items):
    print(x)