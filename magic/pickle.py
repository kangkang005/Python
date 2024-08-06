# Pickle 序列化对象
# pickle 是一种 Python 特有的自描述的数据编码。 通过自描述，被序列化后的数据包含每个对象 开始和结束以及它的类型信息。8。些类型的对象是不能被序列化的。这些通常是那些依赖外部系统状态的对象， 比如打开的文 件，网络连接，线程，进程，栈帧等等。 用户自定义类可以通过提供 __getstate__() 和 __setstate__() 方法来绕过这些限制。
# __getstate__: 序列化对象时调用
# __setstate__: 反序列化时被调用
import threading
import time
class Obj:
    def __init__(self, n):
        self.n = n
        self.thread = threading.Thread(target=self.run)

    def run(self):
        while self.n > 0:
            print(f"current value: {self.n}")
            self.n - 1


o = Obj(1) # Obj不支持序列化，会报错
# import pickle
# d = pickle.dumps(o)
# no = pickle.loads(d)
# print(no.n)


class PickleObj:
    def __init__(self, n):
        self.n = n
        self.n_bak = n
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        while self.n > 0:
            print(f"current value: {self.n}")
            self.n -= 1
            time.sleep(1)

    def __getstate__(self):
        print("__getstate__ called")
        return self.n_bak

    def __setstate__(self, n):
        print("__setstate__ called")
        self.__init__(n)

o = PickleObj(3)
time.sleep(4)
import pickle
d = pickle.dumps(o)
no = pickle.loads(d)