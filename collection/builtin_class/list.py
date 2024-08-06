class MyList(list):
    def __init__(self, *args):
        super().__init__(*args)

    def find(self, element):
        for index, elem in enumerate(self):
            if elem == element:
                return index
        return False

    def flatten(self, inplace=False):
        def dfs(iteration):
            if isinstance(iteration, list):
                for elem in iteration:
                    yield from dfs(elem)
            else:
                yield iteration
        tmp = dfs(self)
        if not inplace:
            return type(self)(tmp)
        self[:] = tmp
        return self

    def format(self, fmt, inplace=False):
        return self.map(fmt, inplace)

    def map(self, args, inplace=False):
        tmp = map(args, self)
        if not inplace:
            return type(self)(tmp)
        self[:] = tmp
        return self

    def filter(self, args, inplace=False):
        tmp = filter(args, self)
        if not inplace:
            return type(self)(tmp)
        self[:] = tmp
        return self

    def frequency(self):
        counts = {}
        for item in self:
            counts.setdefault(item, 0)
            counts[item] += 1
        return counts

    def __iadd__(self, elements):
        if isinstance(elements, list):
            self.extend(elements)
        else:
            self.append(elements)
        return self

    def __add__(self, elements):
        if isinstance(elements, list):
            return list.__add__(self, elements) # call parent method 1
        return super().__add__([elements])      # call parent method 2

    def deduplicate(self, inplace=False):
        data = self
        if not inplace:
            data = self.copy()
        l = len(data)
        while (l > 0):
            l -= 1
            i = l
            while i > 0:
                i -= 1
                if data[i] == data[l]:
                    del data[l]
                    break
        return data

    def duplicate(self, inplace=False):
        duplicates = type(self)()
        for i in range(len(self)):
            count = 0
            for j in range(i+1, len(self)):
                if self[i] == self[j]:
                    count += 1
            if count > 0 and self[i] not in duplicates:
                duplicates.append(self[i])
        if not inplace:
            return duplicates
        self[:] = duplicates[:]
        return self

L = MyList(range(5))
print(L)
print(L[0])
L.extend(range(3))
print(L)
L += [1,11]  # list
L += 10     # int
print(L)

print(L + [1,2])  # list
print(L + 10)   # int

print("######### frequency ##########")
print(L.frequency())

print("######### find ##########")
print(L.find(11))
print(L.find(12))

print("######### flatten ##########")
L = MyList([1, 2, [3, [4]], 5])
print(L.flatten(inplace=True))
print(L)

print("######### format ##########")
L = MyList([1, 2, 3, 4, 5])
print(L.format(str))
print(L)

print("######### map ##########")
L = MyList([1, 2, 3, 4, 5])
print(L.map(lambda x: 2*x, inplace=True))
print(L)

print("######### filter ##########")
L = MyList([1, 2, 3, 4, 5])
print(L.filter(lambda x: x % 2 == 0))
print(L)

print("######### deduplicate ##########")
L = MyList([1, 1, 2, 2, 3, 4, 5])
print(L.deduplicate())
print(L)

print("######### duplicate ##########")
L = MyList([1, 1, 2, 2, 3, 4, 5])
print(L.duplicate(inplace=True))
print(L)
L = MyList([1, 2, 3, 4, 5])
print(L.duplicate())
print(L)