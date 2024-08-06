from collections import OrderedDict

d = OrderedDict(a=1, b=2, c=3, d=4,e=5)
print(d) # OrderedDict([('a', 1), ('b', 2), ('c', 3), ('d', 4), ('e', 5)])

print("######### popitem ##########")
print(d.popitem(last=True)) # ('e', 5)  pop last
print(d.popitem(last=False)) # ('a', 1) pop head
print(d) # OrderedDict([('b', 2), ('c', 3), ('d', 4)]

print("######### move_to_end ##########")
d.move_to_end(key='c', last=True)
print(d)
d.move_to_end(key="c", last=False)   # move to head
print(d)

print("######### pop ##########")
d.pop("c")
print(d)

print("######### copy ##########")
new_copy = d.copy()
print(new_copy)

print("######### update ##########")
d.update({"a":5, "c": 6})
print(d)

print("######### sort ##########")
d = OrderedDict(sorted(d.items(), key=lambda t: t[0]))  # sort by key
print(d)
d = OrderedDict(sorted(d.items(), key=lambda t: t[1]))  # sort by value
print(d)

print("######### FIFO ##########")
class FIFO(OrderedDict):
    def __init__(self, capacity):
        super(FIFO, self).__init__()
        self._capacity = capacity

    def __setitem__(self, key, value):
        containsKey = 1 if key in self else 0
        if len(self) - containsKey >= self._capacity:
            last = self.popitem(last=False)
            print('remove:', last)
        if containsKey:
            print('set:', (key, value))
        else:
            print('add:', (key, value))
        OrderedDict.__setitem__(self, key, value)

d = FIFO(3)
d["1"] = 1
d["2"] = 2
d["3"] = 3
d["3"] = "b"
d["4"] = 4
print(d)