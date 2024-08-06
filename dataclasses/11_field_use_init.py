from dataclasses import dataclass, field

# 从初始化中省略字段

"""
init 参数如果设置为 False，表示不为这个 field 生成初始化操作，dataclass 提供了 hook——__post_init__
__post_init__在__init__后被调用，我们可以在这里初始化那些需要前置条件的 field。
"""
@dataclass
class Person:
    age   : int
    height: float
    weight: float
    bmi   : int = field(init=False)
    # @ERROR
    # bmi   : int = self.weight / (self.height * self.height)

    def __post_init__(self):
        self.bmi = self.weight / (self.height * self.height)

if __name__ == "__main__":
    wei = Person(12, 1.70, 110)
    print(wei)