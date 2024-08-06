from collections import defaultdict

print("######### lambda ##########")
dd = defaultdict(lambda: 'not exist')
dd['key1'] = 'abc'
print(dd['key1']) # key1 exists
print(dd['key2']) # key2 not exists, return default

print("######### list ##########")
lst = defaultdict(list)
lst["test"].append(1)
lst["test"].append(2)
print(lst)

print("######### counter ##########")
s = 'mississippi'
d = defaultdict(int)
for k in s:
    d[k] += 1
print(d)

print("######### nest default: function ##########")
def nest_dict():
    return defaultdict(nest_dict)
nd = nest_dict()
nd["key1"]["key2"] = 2
print(nd)
print(nd["key1"]["key2"])

print("######### nest default: lambda ##########")
tree = lambda: None
tree = lambda: defaultdict(tree)
t = tree()
t["key1"]["key2"] = 2
print(t)

print("######### nest default: class ##########")
class NestedDefaultDict(defaultdict):
    def __init__(self, *args, **kwargs):
        super(NestedDefaultDict, self).__init__(NestedDefaultDict, *args, **kwargs)

    def __repr__(self):
        return repr(dict(self))

t = NestedDefaultDict()
t["key1"]["key2"] = 2
print(t)

print("######### nest default: function ##########")
def nested_defaultdict(existing=None, **kwargs):
    if existing is None:
        existing = {}
    if isinstance(existing, list):
        existing = [nested_defaultdict(val) for val in existing]
    if not isinstance(existing, dict):
        return existing
    existing = {key: nested_defaultdict(val) for key, val in existing.items()}
    return defaultdict(nested_defaultdict, existing, **kwargs)

t = nested_defaultdict()
t["key1"][1] = 2
print(t)

print("######### nest default: depth ##########")
def ddict(some_type, depth=0):
    if depth == 0:
        return defaultdict(some_type)
    else:
        return defaultdict(lambda: ddict(some_type, depth-1))

m = ddict(int, depth=2)
m['a']['b']['c'] += 1
print(m)

print("######### nest dict: function ##########")
class NestedDict(dict):
    def __getitem__(self, key):
        if key in self: return self.get(key)
        return self.setdefault(key, NestedDict())

m = NestedDict()
m['a']['b']['c'] = 1
print(m)