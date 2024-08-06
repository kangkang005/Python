from contextlib import contextmanager
# 从生成器到上下文管理器:
# 通过用 __enter__() 和 __exit__() 方法编写类来创建上下文管理器的传统方式并不困难。
# 但是，有时候完全写出所有内容对于一些微不足道的上下文来说是没有必要的。在这些情况下，
# 使用 contextmanager() 装饰器将生成器函数转换为上下文管理器。

@contextmanager
def make_context():
    # before
    print('entering')
    try:
        # main
        yield {}    # 赋值给 with 语句块的 as 后面的变量
    except RuntimeError as err:
        print('ERROR:', err)
    finally:
        # after
        print('exiting')


if __name__ == "__main__":
    with make_context() as m:
        print(m)
        print("I am Main.")