from typing import Optional

# Optional[X] like Union[X, None]
def hello(name: Optional[str]) -> None:
    # expect str or None
    if name is not None:
        print(name, "Hello")
    else:
        print("I dont know")


hello("wei")
hello(None)
hello(10086)    # not expect