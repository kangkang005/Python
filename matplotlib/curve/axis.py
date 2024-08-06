# %%
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# %%
print("############### label ####################")
zhfont1 = matplotlib.font_manager.FontProperties(fname="SourceHanSansSC-Bold.otf")
title_font = {
    'color': 'blue',
    'size' : 20
}
plt.plot(np.array([1, 2, 3, 4]), np.array([1, 4, 9, 16]))
plt.title("测试", fontproperties = zhfont1, fontdict = title_font)
plt.xlabel("x - 轴", fontproperties = zhfont1)
plt.ylabel("y - label", fontsize=12, color='r')
plt.show()

# %%
print("############### font ####################")
fonts = sorted([f.name for f in matplotlib.font_manager.fontManager.ttflist])
print(fonts)

# %%
# STFangsong (仿宋）、Heiti TC（黑体）
plt.rcParams['font.family']=['STFangsong']
plt.plot(np.array([1, 2, 3, 4]), np.array([1, 4, 9, 16]))
plt.title("TITLE")
plt.xlabel("x - 轴")
plt.ylabel("y - label")
plt.show()

# %%
plt.plot(np.array([1, 2, 3, 4]), np.array([1, 4, 9, 16]))
plt.title("test", loc="left")
plt.xlabel("x - label", loc="left")
plt.ylabel("y - label", loc="top")
plt.show()
# %%
