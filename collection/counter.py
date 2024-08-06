from collections import Counter

c = Counter()
for i in 'sfsadfsdjklgsdla':
    c[i] +=  1

print(isinstance(c,Counter)) # True
print(isinstance(c,dict)) # True
print(c) # Counter({'s': 4, 'd': 3, 'f': 2, 'a': 2, 'l': 2, 'j': 1, 'k': 1, 'g': 1})

print("######### string ##########")
c2 = Counter('asfjslfjsdlfjgkls')
print(c2) # Counter({'s': 4, 'd': 3, 'f': 2, 'a': 2, 'l': 2, 'j': 1, 'k': 1, 'g': 1})

print("######### list ##########")
c = Counter(['red', 'blue', 'red', 'green', 'blue', 'blue'])
print(c) # Counter({'blue': 3, 'red': 2, 'green': 1})

print("######### elements ##########")
c = Counter(a=4, b=2, c=0, d=-2)
print(sorted(c.elements())) # ['a', 'a', 'a', 'a', 'b', 'b']

print("######### most_common ##########")
c = Counter('abracadabra')
print(c.most_common(3)) # [('a', 5), ('b', 2), ('r', 2)]

print("######### subtract ##########")
c = Counter(a=4, b=2, c=0, d=-2)
d = Counter(a=1, b=2, c=3, d=4)
print(c)
print(d)
c.subtract(d)
print(c) # Counter({'a': 3, 'b': 0, 'c': -3, 'd': -6})