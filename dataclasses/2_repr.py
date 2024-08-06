from dataclasses import dataclass

class Person:
    def __init__(self, name, age = 0):
        self.name = name
        self.age  = 0

# dataclass 会自动添加一个__repr__函数，这样我们就不必手动实现它了。
@dataclass
class Person_dataclass:
    name: str
    age : int = 0

if __name__ == "__main__":
    wei = Person(name="wei")
    li  = Person_dataclass(name="li")
    print(wei)
    print(li)