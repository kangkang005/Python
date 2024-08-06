"""
yield from 后面需要加的是可迭代对象，它可以是普通的可迭代对象，也可以是迭代器，甚至是生成器。
"""
def generator_1():
    for i in range(3):
        yield i

def generator_2():
    yield from range(3)

def generator_3():
    yield from list(range(3))

"""
Python 提供了 yield from 表达式，供外围的生成器函数从嵌套的子迭代器中 yield 值。
"""
def generator_4():
    yield from generator_1()
    yield from generator_2()
    yield from generator_3()
"""
上述的 yield from 会先从嵌套进去的小生成器里面取值，如果该生成器已经用完，那么程序的控制流程将回到 yield from 所在的函数中，并继续进入下一套 yield from 逻辑。
"""

if __name__ == "__main__":
    for i in generator_1():
        print(i)
    print()
    for i in generator_2():
        print(i)
    print()
    for i in generator_3():
        print(i)
    for i in generator_4():
        print(i)