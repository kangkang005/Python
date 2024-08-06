from typing import Any

# uncertain or any type
def process_data(data: Any) -> None:
    print(data)

process_data(42)
process_data("hello")
process_data([1, 2, 3])