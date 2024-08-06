from typing import overload, Union
from typing_extensions import Literal

# reference: https://stackoverflow.com/questions/59359943/python-how-to-write-typing-overload-decorator-for-bool-arguments-by-value
# The first two overloads use Literal[...] so we can have precise return types:
@overload
def myfunc(arg: Literal[True]) -> str: ...

@overload
def myfunc(arg: Literal[False]) -> int: ...

# The last overload is a fallback in case the caller provides a regular bool
@overload
def myfunc(arg: bool) -> Union[str, int]: # Union[str, int] == str | int
    ...

@overload
def myfunc(a: int, b: int) -> int:
    return a+b

def myfunc(arg:bool) -> Union[int, str]:
    if arg: return "something"
    else: return 0

print(myfunc(True))
print(myfunc(False))

# Variables declared without annotations will continue to have an inferred type of 'bool'
variable = True
print(myfunc(variable))