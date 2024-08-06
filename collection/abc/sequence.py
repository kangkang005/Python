# @web: https://www.jianshu.com/p/1a2be5efb19e

# collections.abc 模块是 Python 标准库中的一个模块，
# 它定义了一系列抽象基类（Abstract Base Classes, ABCs）， 用于描述容器类的协议（如序列、映射、迭代器等）。
# 这些抽象基类不仅可以用作类型检查，还可以帮助开发者实现符合特定接口的自定义容器类型。
# 从 Python 3.3 开始，这些抽象基类从 collections 模块移到了 collections.abc 模块，
# 但仍可以通过 collections 模块导入以保持向后兼容性。

# 1、可迭代；
# 2、支持下标访问，即实现了 getitem() 方法，同时定义了 len() 方法，可通过 len () 方法获取长度；
# 3、内置的序列类型：list、str、tuple、bytes；
# 4、dict 同样支持 getitem() 和 len()，但它不归属于序列类型，它是映射类型，因为它不能根据下标查找，只能根据 key 来查找；
# 5、抽象类 collections.abc.Sequence 还提供了很多方法，比如 count ()、index ()、contains()、reversed() 可用于扩展；
# 总结结论：序列一定是一个可迭代对象，但可迭代对象不一定是序列。
from collections import Sequence

class BinaryNode:
    def __init__(self, left=None, right=None, value=None):
        self.left = left
        self.right = right
        self.value = value

class IndexableNode(BinaryNode):
    def _traverse(self):
        if self.left is not None:
            yield from self.left._traverse()
        yield self
        if self.right is not None:
            yield from self.right._traverse()

    def __getitem__(self, index):
        for i, item in enumerate(self._traverse()):
            if i == index:
                return item.value
        raise IndexError(f'Index {index} is out of range')

    def __len__(self):
        for count, _ in enumerate(self._traverse(), 1):
            pass
        return count

root = IndexableNode(value=1)
root.left = IndexableNode(
    left  = IndexableNode(value=20),
    value = 2,
    right = IndexableNode(value=21)
    )
root.right = IndexableNode(value=31)
print(list(root))
print(root[0])
print(20 in root)
print(len(root))

print("############## Sequence ##############")
# Sequence support count() & index()
class BetterNode(IndexableNode, Sequence):
    pass

root = BetterNode(value=1)
root.left = BetterNode(
    left  = BetterNode(value=20),
    value = 2,
    right = BetterNode(value=21)
    )
root.right = BetterNode(value=31)
print(list(root))
print(root.count(31))
print(root.index(21))