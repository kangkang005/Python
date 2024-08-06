# @web: https://zhuanlan.zhihu.com/p/82540467
# Context Manager API
# 上下文管理器负责一个代码块内的资源，从进入块时创建到退出块后清理。
# with 语句启用了上下文管理器，API 涉及两种方法：当执行流进入内部代码块时运行 __enter__() 方法，
# 它返回要在上下文中使用的对象。当执行流离开 with 块时，调用上下文管理器的 __exit__() 方法来清理正在使用的任何资源。
class Context:
    def __init__(self, user):
        self.user = user
        print('__init__()')

    def __enter__(self):
        print('__enter__()')
        print(f'enter {self.user}')
        return self

    # __exit__() 方法接收包含 with 块中引发的任何异常的详细信息的参数。
    def __exit__(self, exc_type, exc_val, exc_tb):
        print('__exit__()')
        print('  exc_type =', exc_type)
        print('  exc_val  =', exc_val)
        print('  exc_tb   =', exc_tb)
        print(f'exit {self.user}')


with Context("Wei"):
    print('Doing work in the context')
    raise RuntimeError('error message handled')

# output
# __init__()
# __enter__()
# Doing work in the context
# __exit__()