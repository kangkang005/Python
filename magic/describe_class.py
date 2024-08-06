#coding:utf-8
# 对象的表示和描述
# __str__：使得可通过 str() 方法获取对象的可读信息，__str__输出的应该是用户关注的容易理解的信息，因此对那些负责与客户交互的类，至少更应该重写__str__方法。
# __repr__: 使得可通过 repr() 方法获取对象的详细信息，包括存储地址等，__str__中的信息是__repr__中的一部分。stackoverflow 上有个回答。1，__str__是面向普通用户的信息，__repr__是面向开发者的信息，倒也形象。如果开发者要输出开发人员足够知悉的属性，就需要重写该方法。
# 重写__repr__方法注意：__repr__方法是实例方法，因此带一个参数 self，也只能带这个参数；
# 输出的信息尽可能满足开发者的要求，信息必须详尽和准确。
# __format__: 定义通过 "prefix {:code}".format (obj) 时实例输出的形式，code 是__format__的参数，用来确定以哪种格式 format, 定制数值或字符串类型时常希望重写此方法
# __hash__: 定义 hash 对象实例的返回值，需要为 1 个整数，默认的 hash 方法根据对象的地址和属性值算出来 int 类型整数为对象的 hash 值。一个对象在其生命周期内，如果保持不变，就是 hashable（可哈希的）。像 int,string 是可哈希的，dict,list 等是不可哈希的。哈希性使得对象可以用作 dictionary 键和 set 成员，因为这些数据结构在内部使用了哈希值。如果要判断 item in set 为 True, 则 item==set中的一个元素且 hash(item)==hash(set中的一个元素)。
# __bool__: 调用 bool() 方法时对象的返回值，需为 True/False。
# __dir__：调用 dir() 方法时对象的返回值，一般不需要重写该方法，但在定义__getattr__时有可能需要重写，以打印动态添加的属性。
# __sizeof__: 定义 sys.getsizeof() 方法调用时的返回，指类的实例的大小，单位是字节，在使用 C 扩展编写 Python 类时比较有用。
formats = {
    "long":"Country Has {c.provinces} Provinces",
    "short":"C H {c.provinces} P",
}
class Country:
    def __init__(self, provinces, name):
        self.provinces = provinces
        self.name = name

    # __str__ 会覆盖 __repr__ 方法
    def __str__(self):
        return f"Country has {self.provinces} provinces"

    def __repr__(self):
        s="In __repr__:\n<{} object at {:#016x}>\n".format(repr(self.__class__),id(self) )
        s+=super().__repr__()
        s+="\n"
        s+=repr(self.__dict__)
        return s

    def __format__(self, code):
        return formats[code].format(c=self)

    def __eq__(self, obj):
        return self.provinces == obj.provinces

    def __hash__(self):
        # return 12
        # return hash(self.name)
        return hash(self.provinces)

    def __bool__(self):
        print(self.name)
        return self.name == "Hunan"

    def __dir__(self):
        l = list(self.__dict__.keys())
        l.append("GDP")
        return l

    def __sizeof__(self):
        print("__sizeof__ called")
        return len(self.__dict__)
c = Country(264, "Hunan")
print(c)
# Country has 264 provinces
d = Country(264, "Henan")
print(hash(c))
# 264
print(hash(d))
# 264
print(c == d)
# True
s = set()
s.add(c)
print(d in s) # 相当于判断：hash(d.name) in set(hash(c.name)), 即 264 in set(264)
# True
print(bool(c), bool(d))
# Hunan
# Henan
# True False
import sys
print(sys.getsizeof(c))
# __sizeof__ called
# 18