# %%
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# %%
# use list
fig, ax = plt.subplots()  # Create a figure containing a single axes.
ax.plot([1, 2, 3, 4], [1, 4, 2, 3]);  # Plot some data on the axes.

# %%
# use np.array
fig, ax = plt.subplots()  # Create a figure containing a single axes.
ax.plot(np.array([1, 2, 3, 4]), np.array([1, 4, 2, 3]));  # Plot some data on the axes.

# %%
xpoints = np.array([0, 6])
ypoints = np.array([0, 100])
plt.plot(xpoints, ypoints)
plt.show()

# %%
# only draw point
xpoints = np.array([0, 6])
ypoints = np.array([0, 100])
plt.plot(xpoints, ypoints, 'o')
plt.show()

# %%
# xaxis default 1...N-1
ypoints = np.array([3, 8, 1, 10, 5, 7])
plt.plot(ypoints)
plt.show()

# %%
# multiple curve
x = np.arange(0,4*np.pi,0.1)   # start,stop,step
y = np.sin(x)
z = np.cos(x)
plt.plot(x,y,x,z)
plt.show()

# %%
print("############# Figure ###############")
fig = plt.figure()  # an empty figure with no Axes
fig, ax = plt.subplots()  # a figure with a single Axes
fig, axs = plt.subplots(2, 2)  # a figure with a 2x2 grid of Axes

# %%
print("############# save ###############")
ypoints = np.array([3, 8, 1, 10, 5, 7])
plt.plot(ypoints)
plt.show()
plt.savefig("curve.png",bbox_inches="tight")