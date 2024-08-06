from dataclasses import dataclass, field

# 使用部分字段进行数据表示

# field 中的 repr 参数控制一个字段是否应该包含在自动生成的 __repr__ 方法的返回值中
@dataclass(order=True)
class Person:
    # compare=False tells the dataclass to not use field for compare(__eq__, __lt__, __le__, __gt__, and __ge__)
    name   : str = field(compare=False)
    age    : int
    weight : float = field(compare=False)
    height : float = field(compare=False)
    city   : str = field(repr=False, compare=False) # do not use "city" for representation and comparison
    country: str = field(repr=False, compare=False)

if __name__ == "__main__":
    wei = Person("wei", 23, 70, 1.7, "beijing", "beijing")
    li  = Person("li", 100, 65, 1.60, "jiangsu", "suzhou")
    print(wei)
    print(li)
    print(wei < li)