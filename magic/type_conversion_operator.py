# 支持类型转换运算符
# __int__: 支持 int()
# __float__: 支持 float()
# __oct__: 支持 oct()
# __hex__: 支持 hex()
# __index__: 返回 1 个整数，支持作为 list 下标
# __complex__: 支持 complex() 函数
class MyNum(int):
    def __init__(self, x):
        self.x = x

    def __int__(self):
        print("__int__ called")
        return int(self.x)

    def __float__(self):
        print("__float__ called")
        return float(self.x)

    def __oct__(self):
        print("__oct__ called")
        return oct(self.x)

    def __hex__(self):
        print("__hex__ called")
        return hex(self.x)

    def __index__(self):
        print("__index__ called")
        return int(self.x + 1)

    def __complex__(self):
        print("__complex__ called")
        return complex(self.x, self.x)

n = MyNum(1.2)
m = MyNum(2)
a = [1,2,3]
print(int(n))
print(float(n))
print(oct(n))
print(hex(n))
print(a[n])
print(complex(n))