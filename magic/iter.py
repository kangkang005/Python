# @web: https://blog.csdn.net/os373/article/details/121270379#:~:text=5%20%E4%B8%AA%E4%BD%A0%E4%B8%8D%E7%9F%A5%E9%81%93%E7%9A%84%E5%85%B3%E4%BA%8E%20Python%20%E7%B1%BB%E7%9A%84%E6%8A%80%E5%B7%A7%201%201.%20%E5%88%9B%E5%BB%BA%20%E4%B8%80%E4%B8%AA,%E8%BF%AD%E4%BB%A3%E5%99%A8%20%E8%BF%AD%E4%BB%A3%E5%99%A8%E6%98%AF%E5%85%81%E8%AE%B8%E6%82%A8%E8%BF%AD%E4%BB%A3%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E4%B8%AD%E7%9A%84%E6%89%80%E6%9C%89%E5%85%83%E7%B4%A0%E7%9A%84%E7%B1%BB%E3%80%82%20%E8%BF%AD%E4%BB%A3%E5%99%A8%E7%9A%84%E4%B8%80%E4%B8%AA%E4%BE%8B%E5%AD%90%E6%98%AF%20range%20%E5%87%BD%E6%95%B0%EF%BC%9A%E6%82%A8%E5%8F%AF%E4%BB%A5%E8%BF%AD%E4%BB%A3%E6%9F%90%E4%B8%AA%E8%8C%83%E5%9B%B4%E5%86%85%E7%9A%84%E6%89%80%E6%9C%89%E6%95%B4%E6%95%B0%E5%80%BC%EF%BC%88%E4%BE%8B%E5%A6%82%E4%BD%BF%E7%94%A8%20for%20%E5%BE%AA%E7%8E%AF%EF%BC%89%E3%80%82%20
# 迭代器
# 如果你想创建你自己的迭代器，你只需要实现 __next__ 和 __iter__ 方法。
# __iter__ 应该返回迭代器对象（所以它在大多数情况下返回 self）
# __next__ 应该返回数据结构的下一个元素
class Backward():
  def __init__(self, data):
    self.data = data # 我们将要迭代一个列表类型的 data
    self.index = len(self.data)

  def __iter__(self):
    return self

  def __next__(self):
    if(self.index == 0):
      raise StopIteration
    else:
      self.index -= 1
      return self.data[self.index]


if __name__ == "__main__":
    bw = Backward([1,2,3,4,5])
    for elem in bw:
        print(elem)