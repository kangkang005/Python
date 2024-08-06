# 上下文管理
# python 中使用 with 语句执行上下文管理，处理内存块被创建时和内存块执行结束时上下文应该执行的操作，上下文即程序执行操作的环境，包括异常处理，文件开闭。有两个魔术方法负责处理上下文管理。
# __enter__: 上下文创建时执行的操作，该方法返回 as 后面的对象。
# __exit__：上下文结束时执行的操作
class Closer:
    '''A context manager to automatically close an object with a close method
    in a with statement.'''

    def __init__(self, obj):
        self.obj = obj

    # `with self as x:` `with` 语句上下文管理
    def __enter__(self):
        print('__enter__ called')
        return self.obj # bound to target

    # `with self as x:` `with` 语句上下文管理
    def __exit__(self, exception_type, exception_val, trace):
        print('__exit__ called')
        try:

           self.obj.close()
        except AttributeError:
           print('Not closable. here')
           return True

with Closer(open("1.txt", "w")) as f:
    f.write("1")