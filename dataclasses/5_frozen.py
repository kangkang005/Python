from dataclasses import dataclass

"""
当实例化一个 frozen 对象时，任何企图修改对象属性的行为都会引发 FrozenInstanceError。

因此，一个 frozen 实例是一种很好方式来存储：
* 常数
* 设置
这些通常不会在应用程序的生命周期内发生变化，任何企图修改它们的行为都应该被禁止。
"""
@dataclass(frozen=True)
class Number:
    val: int = 0

if __name__ == "__main__":
    a     = Number(1)
    a.val = 2