# -*- coding: utf-8 -*-

"""
DateTime   : 2021/02/18 18:11
Author     : ZhangYafei
Description: 
"""
from pyecharts.charts import WordCloud
from pyecharts import options as opts
from pyecharts.globals import SymbolType
from snapshot_selenium import snapshot
from pyecharts.render import make_snapshot


words = [("能天使", 10000), ("拉普兰德", 6181), ("艾雅法拉", 4386), ("银灰", 4055),
         ("德克萨斯", 2467), ("麦哲伦", 2244), ("伊芙利特", 1868), ("推进之王", 1484),
         ("煌", 1112), ("黑", 865), ("赫拉格", 847), ("风笛", 582), ("莫斯提玛", 555),
         ("空", 550), ("豆子龙", 462), ("斯卡蒂", 366), ("陨星", 360), ("白金之星", 282),
         ("天火", 273), ("塞雷亚", 265), ("星熊", 569), ("闪灵", 3598), ("夜莺", 1889),
         ]

wordcloud = WordCloud(init_opts=opts.InitOpts(width='800px', height='600px'))
wordcloud.add("", words, word_size_range=[20, 100], shape=SymbolType.DIAMOND)
make_snapshot(snapshot, wordcloud.render('词云图示例.html'), '词云图.png')
