# 支持算术运算符
# __add__: 支持 +
# __sub__: 支持 -
# __mul__: 支持 *
# __matmul__: 支持 @，矩阵乘法，Python3.5 后引入的新特性，支持 numpy 数组表示的矩阵乘法
# __truediv__: 支持 /, __div__是 Python2中的属性，Python3 中用__truediv__
# __floordiv__: 支持 //
# __mod__: 支持 %，取余
# __divmod__: 支持 divmod() 方法，返回 tuple(x//y,x%y)
# __pow__: 支持 **
# __lshift__: 支持左移位 <<
# __rshift__: 支持右移位 >>
# __and__: 支持 &, 按位与
# __or__: 支持 |，按位或
# __xor__: 支持 ^, 按位异或
class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, obj):
        print("__add__ called")
        return (self.x + obj.x, self.y + obj.y)

    def __sub__(self, obj):
        print("__sub__ called")
        return (self.x - obj.x, self.y - obj.y)

    def __mul__(self, obj):
        print("__mul__ called")
        return (self.x * obj.x, self.y * obj.y)

    def __matmul__(self, obj):
        import numpy as np
        print("__matmul__ called")
        return np.array([self.x, obj.x]) @ np.array([self.y, obj.y])

    def __floordiv__(self, obj):
        print("__floordiv__ called")
        return (self.x // obj.x, self.y // obj.y)

    def __truediv__(self, obj):
        print("__div__ called")
        return (self.x / obj.x, self.y / obj.y)

    def __mod__(self, obj):
        print("__mod__ called")
        return (self.x % obj.x, self.y % obj.y)

    def __divmod__(self, obj):
        print("__divmod__ called")
        return (divmod(self.x, obj.x), divmod(self.y, obj.y))

    def __pow__(self, obj):
        print("__pow__ called")
        return (self.x ** obj.x, self.y ** obj.y)

    def __lshift__(self, obj):
        print("__lshift__ called")
        return (self.x << obj.x, self.y << obj.y)

    def __rshift__(self, obj):
        print("__rshift__ called")
        return (self.x >> obj.x, self.y >> obj.y)

    def __and__(self, obj):
        print("__and__ called")
        return (self.x & obj.x, self.y & obj.y)

    def __or__(self, obj):
        print("__or__ called")
        return (self.x | obj.x, self.y | obj.y)

    def __xor__(self, obj):
        print("__xor__ called")
        return (self.x ^ obj.x, self.y ^ obj.y)

p1 = Point2D(8, 16)
p2 = Point2D(1, 3)

print(p1 + p2)
print(p1 - p2)
print(p1 * p2)
print(p1 @ p2)
print(p1 / p2)
print(p1 // p2)
print(p1 % p2)
print(divmod(p1, p2))
print(p1 ** p2)
print(p1 << p2)
print(p1 >> p2)
print(p1 & p2)
print(p1 | p2)
print(p1 ^ p2)