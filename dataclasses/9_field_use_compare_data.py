from dataclasses import dataclass, field

# 使用部分字段进行数据比较

@dataclass(order=True)
class Person:
    # compare=False tells the dataclass to not use field for compare(__eq__, __lt__, __le__, __gt__, and __ge__)
    name  : str = field(compare=False)
    age   : int
    weight: float = field(compare=False)
    height: float = field(compare=False)

    # 自动生成的比较方法会比较一下的数组：
    # (self. age, )

if __name__ == "__main__":
    wei = Person("wei", 23, 70, 1.7)
    li  = Person("li", 100, 65, 1.60)
    print(wei < li)