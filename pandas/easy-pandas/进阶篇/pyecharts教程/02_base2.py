# -*- coding: utf-8 -*-

"""
DateTime   : 2021/02/18 17:34
Author     : ZhangYafei
Description: 
"""
# 虚假数据
from pyecharts.charts import Bar

x_data = ['Apple', 'Huawei', 'Xiaomi', 'Oppo', 'Vivo', 'Meizu']
y_data = [123, 153, 89, 107, 98, 23]


bar = (Bar()
       .add_xaxis(x_data)
       .add_yaxis('', y_data)
      )

bar.render_notebook()