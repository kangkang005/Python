from typing import Dict, Tuple, Sequence, List, Union

Vector = List[Dict[str, Union[str, int]]]

# so boring~
# def print_list(list_data: List[Dict[str, Union[str, int]]]):
def print_list(list_data: Vector):
    print(list_data)

print_list(10086)    # IDE给出非期待类型范围的警告提示，应为类型 'List[List[Union[str, int]]]'，但实际为 'List[int]'
print_list("hello")  # IDE给出非期待类型范围的警告提示，应为类型 'List[List[Union[str, int]]]'，但实际为 'List[int]'

print([{"name": "zhangsan", "age": 18}])  # [{'name': 'zhangsan', 'age': 18}]

############################################################

ConnectionOptions = Dict[str, str]
Address = Tuple[str, int]
Server = Tuple[Address, ConnectionOptions]

def broadcast_message(message: str, servers: Sequence[Server]) -> None:
    pass

# like
def broadcast_message2(
        message: str,
        servers: Sequence[Tuple[Tuple[str, int], Dict[str, str]]]) -> None:
    pass

broadcast_message('OK', [(('127.0.0.1', 8080), {"method": "GET"})])