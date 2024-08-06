# %%
import pandas as pd
import numpy as np

# %%
# index
s1 = pd.Series(["Google", "Runoob", "Wiki"],index=['a','b','c'],name='example')
print(s1)
print(s1['a'])
print(s1[2])

# %%
# list create Series
print("#################")
s2 = pd.Series(["Google", "Runoob", "Wiki"],name='example')
print(s2)
print(s2[0])

# %%
# dict create Series
print("#################")
sites = {1: "Google", 2: "Runoob", 3: "Wiki"}
myvar = pd.Series(sites)
print(myvar)

# %%
# create Series by part of dict
print("#################")
sites = {1: "Google", 2: "Runoob", 3: "Wiki"}
myvar = pd.Series(sites, index = [1, 2])
print(myvar)

# %%
# np array create Series
print("#################")
s = pd.Series(np.array([1, 2, 3, 4]), index=['a', 'b', 'c', 'd'])
print(s)

# %%
print("###### for ######")
for index, value in s.items():
    print(f"Index: {index}, Value: {value}")

# %%
print("###### slice ######")
print(s['a':'c'])
print(s[:3])

# %%
print("###### del ######")
del s['a']
s_dropped = s.drop(['b'])   # delete and return new series
print(s_dropped)

# %%
print("###### filter ######")
s = pd.Series(np.array([10, 20, 30, 40]))
filtered_series = s[s > 15]
print(filtered_series)

# %%
print("###### operation ######")
result = s * 2
print(result)
print("sum=",s.sum())
print("mean=",s.mean())
print("max=",s.max())
print("min=",s.min())
print("std=",s.std())

# %%
print("###### method ######")
index = s.index
print(index)
values = s.values
print(values)
describe = s.describe() # statistics info
print(describe)
max_index = s.idxmax()
min_index = s.idxmin()
print(max_index)
print(min_index)
print(s.dtype)
print(s.shape)
print(s.size)
print(s.head())  # default to head 5
print(s.tail())  # default to tail 5
s = s.astype('float64') # convert to float type
print(s)
print(s.tolist())   # convert to list