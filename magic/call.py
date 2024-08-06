# 可调用对象
# __call__: 对象像函数一样可调用
class Entity:
    def __init__(self, size, x, y):
        self.x, self.y = x, y
        self.size = size

    # `self(args)` “调用”对象时
    def __call__(self, s):
        return self.x*self.y + s

e = Entity(2, 2, 3)
print(e(3))
# like: self.__call__(3)