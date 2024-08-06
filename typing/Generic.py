from typing import TypeVar, Generic

###################  泛型类（Generic Classes） ####################
# 泛型类是可以接受一个或多个泛型类型参数的类。这些参数可以用来指定类的属性类型、方法参数类型、方法返回值类型或类内部使用的其他类型。
T = TypeVar('T')

class Box(Generic[T]):
    def __init__(self, item: T):
        self.item = item

    def get_item(self) -> T:
        return self.item

int_box = Box[int](10)
print(int_box.get_item())  # 输出: 10

str_box = Box[str]("Hello")
print(str_box.get_item())  # 输出: Hello

float_box = Box(12.1)
print(float_box.get_item())  # 输出: 12.1