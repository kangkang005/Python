from typing import Sequence, List

# Sequence，是 collections.abc.Sequence 的泛型，在某些情况下，
# 我们可能并不需要严格区分一个变量或参数到底是列表 list 类型还是元组 tuple 类型，
# 我们可以使用一个更为泛化的类型，叫做 Sequence，其用法类似于 List
def square(elements: Sequence[float]) -> List[float]:
    return [x ** 2 for x in elements]

my_list = [1, 2, 3, 4, 5]
my_tuple = (1, 2, 3)
print(square(my_list))
print(square(my_tuple))