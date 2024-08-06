# 反射算术运算符
# 2.4.3 中的是常规算术运算符，a+b 或者 b+a 都可以进行运算，反射运算符指如 a+b 时，a 中没有定义需调用 b 的运算方法实现运算的运算符。如__radd__, 则要执行此方法 a 中需没有实现__add__和__radd__方法，才会去调用 b 中对应的 r方法3
class Point2DA:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Point2DB:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __radd__(self, obj):
        print("__radd__ called")
        return (self.x + obj.x, self.y + obj.y)

    def __rsub__(self, obj):
        print("__rsub__ called")
        return (self.x - obj.x, self.y - obj.y)

    def __rmul__(self, obj):
        print("__rmul__ called")
        return (self.x * obj.x, self.y * obj.y)

    def __rmatmul__(self, obj):
        import numpy as np
        print("__rmatmul__ called")
        return np.array([self.x, obj.x]) @ np.array([self.y, obj.y])

    def __rfloordiv__(self, obj):
        print("__rfloordiv__ called")
        return (self.x // obj.x, self.y // obj.y)

    def __rtruediv__(self, obj):
        print("__rtruediv__ called")
        return (self.x / obj.x, self.y / obj.y)

    def __rmod__(self, obj):
        print("__rmod__ called")
        return (self.x % obj.x, self.y % obj.y)

    def __rpow__(self, obj):
        print("__rpow__ called")
        return (self.x ** obj.x, self.y ** obj.y)

    def __rlshift__(self, obj):
        print("__rlshift__ called")
        return (self.x << obj.x, self.y << obj.y)

    def __rrshift__(self, obj):
        print("__rrshift__ called")
        return (self.x >> obj.x, self.y >> obj.y)

    def __rand__(self, obj):
        print("__rand__ called")
        return (self.x & obj.x, self.y & obj.y)

    def __ror__(self, obj):
        print("__ror__ called")
        return (self.x | obj.x, self.y | obj.y)

    def __rxor__(self, obj):
        print("__rxor__ called")
        return (self.x ^ obj.x, self.y ^ obj.y)

p1 = Point2DA(3,4)
p2 = Point2DB(2,3)

print(p1 + p2)
print(p1 - p2)
print(p1 * p2)
print(p1 @ p2)
print(p1 / p2)
print(p1 // p2)
print(p1 % p2)
print(p1 ** p2)
print(p1 << p2)
print(p1 >> p2)
print(p1 & p2)
print(p1 | p2)
print(p1 ^ p2)