from dataclasses import dataclass
# Dataclasses 是一些适合于存储数据对象（data object）的 Python 类。
# 数据对象存储并表示特定的数据类型。

# @web: https://zhuanlan.zhihu.com/p/59657729
# @web: https://www.cnblogs.com/apocelipes/p/10284346.html
# @web: https://blog.csdn.net/raelum/article/details/136680946
class Number:
    def __init__(self, val = 1):
        self.val = val

# same as Number
@dataclass
class Number_dataclass:
    val:int = 0

if __name__ == "__main__":
    one = Number()
    print(one.val)
    two   = Number_dataclass(2)
    print(two.val)