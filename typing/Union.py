from typing import Union

def process_data(data: Union[int, str]) -> None:
    print(data)

process_data(42)
process_data("hello")
process_data([1, 2, 3])   # 传入列表（再次强调，类型注解不强制要求必须与此匹配）
# 与注解类型不匹配依旧可以存储数据或执行函数，但IDE会给出“非期待类型”的警告