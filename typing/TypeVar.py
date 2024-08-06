from typing import TypeVar, List, Union

################ 泛型类型变量（Generic Type Variables） ##############
# 定义一个泛型类型变量，用于表示某种不确定的类型。泛型类型变量通常使用大写字母命名，比如 T、U、V 等。
T = TypeVar('T')

def first_element(items: List[T]) -> T:
    return items[0]

int_list = [1, 2, 3, 4, 5]
print(first_element(int_list))  # 输出: 1

str_list = ["Hello", "World", "Python"]
print(first_element(str_list))  # 输出: Hello


################ 泛型约束（Generic Constraints）#####################
# 希望泛型类型只能是特定的类型或其子类
T = TypeVar('T', int, float)

def sum_values(items: List[T]) -> Union[int, float]:
    return sum(items)

int_list = [1, 2, 3, 4, 5]
print(sum_values(int_list))  # 输出: 15

float_list = [1.5, 2.5, 3.5, 4.5, 5.5]
print(sum_values(float_list))  # 输出: 16.0