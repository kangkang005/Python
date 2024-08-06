from dataclasses import dataclass

# 我们不需要定义__eq__和__lt__方法，因为当 order = True 被调用时，dataclass 装饰器会自动将它们添加到我们的类定义中。
@dataclass(order=True)
class Person:
    name: str
    age : int = 0

"""
自动生成的__eq__方法等同于：
def __eq__(self, other):
    return (self.name, self.age) == (other.name, other.age)

请注意属性的顺序。它们总是按照你在 dataclass 类中定义的顺序生成。
同样，等效的__le__函数类似于：
def __le__(self, other):
    return (self.name, self.age) <= (other.name, other.age)
"""

if __name__ == "__main__":
    wei     = Person("wei", 12)
    li      = Person("li", 12)
    old_wei = Person("wei", 100)
    print(wei == li)
    print(wei != li)
    print(wei > old_wei)
    print(wei >= old_wei)