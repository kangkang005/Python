# @web: https://zhuanlan.zhihu.com/p/26487659
from contextlib import contextmanager

@contextmanager
def my_open(path, mode):
    f = open(path, mode)
    yield f
    f.close()

with my_open("create_class.py", 'r') as f:
    for line in f:
        print(line)