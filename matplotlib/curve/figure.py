# %%
# Figure 对象是整个图形的容器，Axes 对象是具体子图的容器。
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# %%
print("############### size ####################")
fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
current_size = fig.get_size_inches()
print("Current Size:", current_size)
# set figure size
fig.set_size_inches(8, 4, forward=True)
updated_size = fig.get_size_inches()
print("Updated Size:", updated_size)
plt.show()

# %%
print("############### dpi ####################")
fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
current_dpi = fig.get_dpi()
print("Current DPI:", current_dpi)
# set dpi
fig.set_dpi(150)
updated_dpi = fig.get_dpi()
print("Updated DPI:", updated_dpi)
plt.show()

# %%
print("############### background ####################")
fig = plt.figure()
# set background
fig.set_facecolor('red')
ax = fig.add_subplot()
ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
plt.show()

# %%
print("############### edge color ####################")
fig = plt.figure()
fig.set_edgecolor('green')
fig.set_linewidth(4)
ax = fig.add_subplot()
ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
plt.show()

# %%
print("############### transparency ####################")
fig = plt.figure()
fig.patch.set_facecolor('red')
fig.patch.set_alpha(0.3)
ax = fig.add_subplot()
ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
plt.show()

# %%
print("############### edge width ####################")
fig = plt.figure()
fig.set_edgecolor('red')
fig.set_linewidth(20)
ax = fig.add_subplot()
ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
plt.show()

# %%
print("############### axes ####################")
# add_axes([left, bottom, width, height]), 0~1
fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
ax.plot([0, 1], [0, 1])
ax.set_title('Custom Painting')

# %%
fig = plt.figure()
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])  # 左、底、宽、高的比例
ax2 = fig.add_axes([0.2, 0.5, 0.4, 0.3])  # 左、底、宽、高的比例
ax1.plot([1, 2, 3, 4], [10, 20, 25, 30], label='Subplot 1')
ax2.plot([1, 2, 3, 4], [30, 25, 20, 10], label='Subplot 2')
ax1.legend()
ax2.legend()
plt.show()

# %%
print("############### subplot ####################")
# add_subplot(rows, cols, index), from left to right, from top to bottom
fig = plt.figure()
ax1 = fig.add_subplot(2, 2, 1)
ax1.plot([0, 1], [0, 1])
ax1.set_title('Painting 1')
ax4 = fig.add_subplot(2, 2, 4)
ax4.plot([0, 1], [0, -1])
ax4.set_title('Painting 4')
plt.tight_layout()
plt.show()

# %%
print("############### Custom Figure subclasses: watermark ####################")
from matplotlib.figure import Figure

class WatermarkFigure(Figure):
    """A figure with a text watermark."""

    def __init__(self, *args, watermark=None, **kwargs):
        super().__init__(*args, **kwargs)

        if watermark is not None:
            bbox = dict(boxstyle='square', lw=3, ec='gray',
                        fc=(0.9, 0.9, .9, .5), alpha=0.5)
            self.text(0.5, 0.5, watermark,
                      ha='center', va='center', rotation=30,
                      fontsize=40, color='gray', alpha=0.5, bbox=bbox)


x = np.linspace(-3, 3, 201)
y = np.tanh(x) + 0.1 * np.cos(5 * x)

plt.figure(FigureClass=WatermarkFigure, watermark='Watermark')
plt.plot(x, y)

# %%
print("############### Figure size in different units ####################")
# Figure size in inches(default)
text_kwargs = dict(ha='center', va='center', fontsize=28, color='C1')
plt.subplots(figsize=(6, 2))
plt.text(0.5, 0.5, '6 inches x 2 inches', **text_kwargs)
plt.show()

# %%
# Figure size in centimeter
cm = 1/2.54  # centimeters in inches
plt.subplots(figsize=(15*cm, 5*cm))
plt.text(0.5, 0.5, '15cm x 5cm', **text_kwargs)
plt.show()

# %%
# Figure size in pixel
px = 1/plt.rcParams['figure.dpi']  # pixel in inches
plt.subplots(figsize=(600*px, 200*px))
plt.text(0.5, 0.5, '600px x 200px', **text_kwargs)
plt.show()