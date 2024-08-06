import inspect
from pprint import *

# stack() 获取的就是 frame 的列表，是一个按照调用顺序包含了所有栈帧的列表。
def show_stack():
    for level in inspect.stack():
        print("{}[{}]\n -> {}".format(level.frame.f_code.co_filename,
                                      level.lineno,
                                      level.code_context[level.index].strip()))
        pprint(level.frame.f_locals)
        print("\n")

def recurse(limit):
    local_variable = "." * limit
    if limit <= 0:
        show_stack()
        return
    recurse(limit - 1)
    return local_variable

if __name__ == '__main__':
    recurse(2)