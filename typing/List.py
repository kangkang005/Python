from typing import List

int_list: List[int] = [3, 5, 9, 7, 1]
str_list: List[str] = ["hello", "world"]

def sort_numbers(numbers: List[int]) -> List[int]:
    return sorted(numbers)


print(sort_numbers(int_list))  # [1, 3, 5, 7, 9]