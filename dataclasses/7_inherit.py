from dataclasses import dataclass

@dataclass
class Person:
    age : int = 0
    name: str = ""
    def __post_init__(self):
        print("Person")

# Student 的参数是在类中定义的字段的顺序。
@dataclass
class Student(Person):
    grade: int = 0
    def __post_init__(self):
        super().__post_init__() # 调用 Person 的 post_init
        print("Student")

if __name__ == "__main__":
    s = Student(20, "John Doe", 12)
    print(s)