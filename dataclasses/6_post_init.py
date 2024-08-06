from dataclasses import dataclass
import math
class Float:
    def __init__(self, val = 0):
        self.val = val
        self.process()
    def process(self):
        self.decimal, self.integer = math.modf(self.val)

# 生成的__init__方法在返回之前调用__post_init__返回。
@dataclass
class FloatNumber:
    val: float = 0.0
    def __post_init__(self):
        self.decimal, self.integer = math.modf(self.val)

if __name__ == "__main__":
    a = Float(2.2)
    print(a.decimal)
    print(a.integer)
    print(a)

    b = FloatNumber(2.2)
    print(b.decimal)
    print(b.integer)
    print(b)