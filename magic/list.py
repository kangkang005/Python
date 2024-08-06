# 定制个性化序列
# 定义一个不可变容器，只需要实现__len__和__getitem__, 可变容器在此基础上还需实现__setitem__和__delitem__, 如果希望容器是可迭代的，还需实现__iter__方法。
# __len__: 返回序列的长度，支持 len()
# __getitem__: 支持 self[key]
# __setitem__: 支持 self[key]=value
# __delitem__: 支持 del self[key]
# __iter__: 支持 for item in self
# __reversed__: 支持 reversed() 方法
# __contains__: 支持 in 判断
# __missing__: 当定制序列是 dict 的子类时，使用 dict[key] 读取元素而 key 没有定义时调用。
class FunctionalList:

    def __init__(self, values=None):
        if values is None:
            self.values = []
        else:
            self.values = values

    def __len__(self):
        return len(self.values)

    # `self[key]` 使用索引访问元素时
    def __getitem__(self, key):
        # if key is of invalid type or value, the list values will raise the error
        return self.values[key]

    # `self[key] = val` 对某个索引值赋值时
    def __setitem__(self, key, value):
        self.values[key] = value

    # `del self[key]` 删除某个索引值时
    def __delitem__(self, key):
        del self.values[key]

    # `for x in self` 迭代时
    def __iter__(self):
        return iter(self.values)

    def __reversed__(self):
        return reversed(self.values)

    # `value in self`, `value not in self` 使用 `in` 操作测试关系时
    def __contains__(self, val):
        print("__contains__ called")
        return True if val in self.values else False

    def append(self, value):
        self.values.append(value)
    def head(self):
        # get the first element
        # 取得第一个元素
        return self.values[0]
    def tail(self):
        # get all elements after the first
        # 取得除第一个元素外的所有元素
        return self.values[1:]
    def init(self):
        # get elements up to the last
        # 取得除最后一个元素外的所有元素
        return self.values[:-1]
    def last(self):
        # get last element
        # 取得最后一个元素
        return self.values[-1]
    def drop(self, n):
        # get all elements except first n
        # 取得除前n个元素外的所有元素
        return self.values[n:]
    def take(self, n):
        # get first n elements
        # 取得前n个元素
        return self.values[:n]

l = FunctionalList()
l.append(2)
l.append(5)
l.append(4)
print(l)
for i in l:
    print(i)
del l[1]
print(2 in l)
for i in l:
    print(i)
print(l[0])
l = reversed(l)
for i in l:
    print(i)