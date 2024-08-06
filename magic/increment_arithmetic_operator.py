# 自增算术运算符
# 自增运算符：执行相应运算，并将结果赋予左值，如 a+=b。
class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iadd__(self, other):
        print("__iadd__ called")
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        print("__isub__ called")
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, other):
        print("__imul__ called")
        self.x *= other.x
        self.y *= other.y
        return self

    def __imatmul__(self, other):
        print("__imatmul__ called")
        import numpy as np
        v = np.array([self.x, other.x]) @ np.array([self.y, other.y])
        self.x = v
        self.y = v
        return self

    def __itruediv__(self, other):
        print("__itruediv__ called")
        self.x /= other.x
        self.y /= other.y
        return self

    def __ifloordiv__(self, other):
        print("__ifloordiv__ called")
        self.x //= other.x
        self.y //= other.y
        return self

    def __imod__(self, other):
        print("__imod__ called")
        self.x %= other.x
        self.y %= other.y
        return self

    def __ipow__(self, other):
        print("__ipow__ called")
        self.x **= other.x
        self.y **= other.y
        return self

    def __ilshift__(self, other):
        print("__ilshift__ called")
        self.x <<= other.x
        self.y <<= other.y
        return self

    def __irshift__(self, other):
        print("__irshift__ called")
        self.x >>= other.x
        self.y >>= other.y
        return self

    def __iand__(self, other):
        print("__iand__ called")
        self.x &= other.x
        self.y &= other.y
        return self

    def __ixor__(self, other):
        print("__ixor__ called")
        self.x |= other.x
        self.y |= other.y
        return self

    def __ior__(self, other):
        print("__ior__ called")
        self.x ^= other.x
        self.y ^= other.y
        return self

p1 = Point2D(2,3)
p2 = Point2D(3,4)

p1 += p2
print(p1.x, p1.y)
p1 -= p2
print(p1.x, p1.y)
p1 *= p2
print(p1.x, p1.y)
p1 @= p2
print(p1.x, p1.y)
p1 /= p2
print(p1.x, p1.y)
p1 = p2
print(p1.x, p1.y)
p1 //= p2
print(p1.x, p1.y)
p1 %= p2
print(p1.x, p1.y)
p1 **= p2
print(p1.x, p1.y)
p1 <<= p2
print(p1.x, p1.y)
p1 >>= p2
print(p1.x, p1.y)
p1 &= p2
print(p1.x, p1.y)
p1 |= p2
print(p1.x, p1.y)
p1 ^= p2
print(p1.x, p1.y)