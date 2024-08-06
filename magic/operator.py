# 在定制类对象间支持使用运算符号
# 支持比较运算符号
# __eq__(self, obj): 支持 ==
# __ne__(self, obj): 支持 ==
# __le__(self, obj): 支持 <=
# __ge__(self, obj): 支持 >=
# __lt__(self, obj): 支持 <
# __gt__(self, obj): 支持 >
class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __square_sum(self, obj:Point3D):
        return sum([pow(getattr(obj, k), 2) for k in obj.__dict__])

    def __eq__(self, obj):
        print("equal called")
        d1 = self.__square_sum(self)
        d2 = self.__square_sum(obj)
        return d1 == d2

    def __ne__(self, obj):
        print("not equal called")
        d1 = self.__square_sum(self)
        d2 = self.__square_sum(obj)
        return d1 != d2

    def __le__(self, obj):
        print("not equal called")
        d1 = self.__square_sum(self)
        d2 = self.__square_sum(obj)
        return d1 <= d2

    def __ge__(self, obj):
        print("not equal called")
        d1 = self.__square_sum(self)
        d2 = self.__square_sum(obj)
        return d1 >= d2

    def __lt__(self, obj):
        print("less than called")
        d1 = self.__square_sum(self)
        d2 = self.__square_sum(obj)
        return d1 < d2

    def __gt__(self, obj):
        print("great than called")
        d1 = self.__square_sum(self)
        d2 = self.__square_sum(obj)
        return d1 > d2
p1 = Point3D(1,2,3)
p2 = Point3D(2,2,3)
print(p1 == p2)
print(p1 != p2)
print(p1 <= p2)
print(p1 >= p2)
print(p1 > p2)
print(p1 < p2)