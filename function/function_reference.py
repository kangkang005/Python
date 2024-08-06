# 函数引用
import operator
op = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}

add = op["+"]
print("add 1, 2 =", add(1,2))
print("op[\"+\"] 1, 2 =", op["+"](1,2))

def operation(func, *args):
    print(func(*args))

operation(operator.add, 1, 2)
operation(operator.mul, 1, 2)