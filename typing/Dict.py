from typing import Dict, Union

# Dict[key, value]
string_int_dict: Dict[str, int] = {"one": 1, "two": 2}
int_string_dict: Dict[int, str] = {1: "one", 2: "two"}


def user_info(name: str, age: int) -> Dict[str, Union[str, int]]:
    user = {}
    user['name'] = name
    user['age'] = age
    return user

print(user_info("wei", 18))  # {'name': 'wei', 'age': 18}