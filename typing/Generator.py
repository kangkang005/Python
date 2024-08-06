'''
它的声明比较特殊，其后的中括号紧跟着三个参数；

YieldType：yield 关键字后面紧跟的变量类型；
SendType：yield 返回的结果类型；
ReturnType：最后生成器 return 的结果类型；
通常生成器只需要 yieldType 参数，不需要 SendType 和 ReturnType 可以将其设置为空；
'''
from typing import Generator, Iterable, TypeVar

# 定义一个泛型变量，表示生成器返回的元素类型
T = TypeVar('T')

# 定义一个生成器函数，它接受一个可迭代对象，并逐个产生其元素
def generate_elements(iterable: Iterable[T]) -> Generator[T, None, None]:
    for item in iterable:
        yield item

# 使用示例
# 创建一个整数生成器
int_generator: Generator[int, None, None] = generate_elements([1, 2, 3, 4, 5])

# 使用生成器
for number in int_generator:
    print(number)
# 输出:
# 1
# 2
# 3
# 4
# 5

# 创建一个字符串生成器
str_generator: Generator[str, None, None] = generate_elements(["hello", "world"])

# 使用生成器
for word in str_generator:
    print(word)
# 输出:
# hello
# world