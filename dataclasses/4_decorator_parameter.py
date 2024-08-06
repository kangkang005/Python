from dataclasses import dataclass

"""
@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)
class C:
    ...

init  : 默认将生成__init__方法。如果传入 False，那么该类将不会有__init__方法。
repr  : __repr__方法默认生成。如果传入 False，那么该类将不会有__repr__方法。
eq    : 默认将生成__eq__方法。如果传入 False，那么__eq__方法将不会被 dataclass 添加，但默认为 object.__eq__。
order : 默认将生成__gt__、__ge__、__lt__、__le__方法。如果传入 False，则省略它们。
frozen: frozen：决定是否冻结实例化后的属性。一旦冻结，任何企图修改对象属性的行为都会引发 FrozenInstanceError。
"""
@dataclass(repr=False)
class Person:
    name: str
    age : int = 0

@dataclass
class Other:
    name: str
    age : int = 0

if __name__ == "__main__":
    wei = Person(name="wei")
    li  = Other(name="li")
    print(wei)
    print(li)