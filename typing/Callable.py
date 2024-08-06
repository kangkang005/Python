from typing import Callable

# Callable[[input1, input2...], output]
def greet(name: str) -> str:
    return f"hello, {name}!"

def register_greeting(name: str, func: Callable[[str], str]) -> None:
    print(func(name))

register_greeting("wei", greet)

def incorrect_greet(age: int) -> str:
    return f"I am {age} age..."

register_greeting(18, incorrect_greet)  # 这将引发IDE的非期待类型范围的警告，因为incorrect_greet的参数类型不匹配