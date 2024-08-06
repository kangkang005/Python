# 支持一元运算符
# __pos__：支持 +, 大多数情况下 +x 依然是 x, 一元运算符 + 没有执行任何操作，如 +(-1) 还是 -1，在__pos__中可以定义 + 的操作。
# __neg__: 支持 - 运算符
# __invert__:~ 符号的逻辑
# __abs__: 定制 abs() 方法调用时的逻辑
# __round__：round() 方法调用时的逻辑
# __floor__：定制 math.floor() 方法调用时的逻辑，譬如向下取整
# __ceil__：定制 math.ceil() 方法调用时的逻辑，譬如向上取整
# __trunc__: 定制 math.trunc() 方法调用时的逻辑
class MyNum(int):
    def __init__(self, x):
        self.x = x

    # `+self` 一元加运算符
    def __pos__(self):
        return abs(self.x)

    # `-self` 一元减运算符
    def __neg__(self):
        return -self.x

    def __abs__(self):
        return pow(self.x,2)

    # `~self` 取反运算符
    def __invert__(self):
        return -1 if self.x > 0 else 1

    def __round__(self, n):
        print(f"{n} digits after point would be remained.")
        return 1 if self.x > 0 else 0

    def __floor__(self):
        return self.x - 1

    def __ceil__(self):
        return self.x + 1

    def __trunc__(self):
        return self.x // 10
a = MyNum(-12)
print(abs(a))
print(+a)
print(~a)
print(-a)
round(a, 10)