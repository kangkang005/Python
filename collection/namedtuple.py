from collections import namedtuple

point = namedtuple('Points', ['x', 'y'])
p1 = point(2, 3)
p2 = point(4, 2)

print(p1) # Points(x=2, y=3)
print(p2) # Points(x=4, y=2)

print("####### isinstance ######")
print(isinstance(p1, point)) # True
print(isinstance(p1, tuple)) # True

print("####### make: assign, not inplace operation ######")
a= [11, 3]
new_p = p1._make(a)
print(new_p) # Points(x=11, y=3)
print(p1)    # Points(x=2, y=3) , not change

print("####### field ######")
print(p1._fields)

print("####### replace, not inplace operation ######")
new_p = p1._replace(y=4.5)
print(new_p) # Points(x=2, y=4.5)
print(p1)    # Points(x=2, y=3), not change

print("####### _asdict: change to OrderedDict, not inplace operation ######")
new_p = p1._asdict()
print(new_p) # {'x': 2, 'y': 3}
print(p1)    # Points(x=2, y=3), not change

print("####### operation ######")
print(p1.x)
print(p1[0])
a, b = p1
print(a, b)

print("####### iteration ######")
for i in p1:
    print(i)

print("####### dict to namedtuple ######")
dict4 = {'x':14, 'y':16}
Point4 = namedtuple("Point4", 'x y')
p4 = Point4(**dict4)
print(p4)