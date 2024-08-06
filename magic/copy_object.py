# 复制对象
# __copy__: 执行 copy.copy() 时调用
# __deepcopy__: 执行 copy.deepcopy() 时调用，见 [7]
# (https://stackoverflow.com/questions/1500718/how-to-override-the-copy-deepcopy-operations-for-a-python-object)
class Obj:
    def __init__(self, x):
        self.x = x
    # 调用 copy.copy()
    def __copy__(self):
        print("__copy__ called")
        return self
    # 调用 copy.deepcopy()
    def __deepcopy__(self, item):
        print("__deepcopy__ called")
        return self