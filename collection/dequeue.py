from collections import deque

limit_q = deque(['a', 'b', 'c'], maxlen=3)
q = deque(['a', 'b', 'c'])
print("########## append ###########")
limit_q.append('d') # limit_q is full, pop first element
q.append('d')
print(limit_q)
print(q)

print("########## appendleft ###########")
limit_q.appendleft('e')
q.appendleft('e')
print(limit_q)
print(q)

print("########## pop ###########")
print(limit_q.pop())
print(q.pop())
print(limit_q)
print(q)

print("########## popleft ###########")
print(limit_q.popleft())
print(q.popleft())
print(limit_q)
print(q)

print("########## copy ###########")
new_copy = limit_q.copy()
print(new_copy)

print("########## extend ###########")
print(limit_q.extend(['i', 'j']))
print(q.extend(['i', 'j']))
print(limit_q)
print(q)

print("########## extendleft ###########")
print(limit_q.extendleft(['i', 'j']))
print(q.extendleft(['i', 'j']))
print(limit_q)
print(q)

print("########## count ###########")
print(q.count("j"))
print(q)

print("########## index ###########")
print(limit_q.index("i"))
print(q.index("i"))

print("########## remove ###########")
limit_q.remove("i")
q.remove("i")
print(limit_q)
print(q)

print("########## reverse ###########")
limit_q.reverse()
q.reverse()
print(limit_q)
print(q)

print("########## maxlen ###########")
print(limit_q.maxlen)
print(q.maxlen)

print("########## rotate ###########")
limit_q.rotate(1)
print(limit_q)