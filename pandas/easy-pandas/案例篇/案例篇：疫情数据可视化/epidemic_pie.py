# -*- coding: utf-8 -*-

"""
DateTime   : 2021/02/18 9:50
Author     : ZhangYafei
Description: 疫情数据可视化
"""
import datetime
import logging
import random

import requests
from pyecharts import options as opts
from pyecharts.charts import Pie
# 导入输出图片工具
from pyecharts.render import make_snapshot
# 使用snapshot-selenium 渲染图片
from snapshot_selenium import snapshot


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


def plot_rose_pie(out_type: str = 'html', filename: str = 'epidemic_rose_pie'):
    url = 'https://lab.isaaclin.cn/nCoV/api/area'
    data_json = requests.get(url).json()
    logging.info('get response success, processing plot data...')
    data = {}
    for item in data_json['results']:
        if item['countryEnglishName']:
            if item['deadCount'] is not None and item['countryName'] is not None:
                data[item['countryName']] = item['deadCount']

    data = dict(sorted(data.items(), key=lambda k: k[1], reverse=True))

    # 名称有重复的，把国家名作为 key 吧
    country_list = list(data.keys())[:10]
    count_list = list(data.values())[:10]
    logging.info('data processing completed, ready to draw...')

    # 随机颜色生成
    def randomcolor(kind):
        colors = []
        for i in range(kind):
            colArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
            color = ""
            for i in range(6):
                color += colArr[random.randint(0, 14)]
            colors.append("#" + color)
        return colors


    color_series = randomcolor(len(count_list))
    # 创建饼图
    pie = Pie(init_opts=opts.InitOpts(width='800px', height='900px'))
    # 添加数据
    pie.add("", [list(z) for z in zip(country_list, count_list)],
            radius=['20%', '100%'],
            center=['60%', '65%'],
            rosetype='area')
    # 设置全局配置
    # pie.set_global_opts(title_opts=opts.TitleOpts(title='南丁格尔玫瑰图'),
    #                     legend_opts=opts.LegendOpts(is_show=False))
    # 设置全局配置项
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    pie.set_global_opts(title_opts=opts.TitleOpts(title='全球新冠疫情', subtitle=f'死亡人数最多\n 的10个国家\n\n{date}',
                                                  title_textstyle_opts=opts.TextStyleOpts(font_size=15, color='#0085c3'),
                                                  subtitle_textstyle_opts=opts.TextStyleOpts(font_size=12, color='#003399'),
                                                  pos_right='center', pos_left='53%', pos_top='62%', pos_bottom='center'
                                                  ),
                        legend_opts=opts.LegendOpts(is_show=False))
    # 设置系列配置和颜色
    pie.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position='inside', font_size=12,
                                                  formatter='{b}：{c}', font_style='italic',
                                                  font_family='Microsoft YaHei'))
    pie.set_colors(color_series)
    filename = filename.split('.')[0]
    if out_type == 'html':
        pie.render(f'{filename}.html')
    else:
        make_snapshot(snapshot, pie.render(), f'{filename}.{out_type}')
    logging.info(f'{filename}.{out_type} saved success...')


if __name__ == '__main__':
    plot_rose_pie(out_type='png', filename='epidemic_rose_pie')
    # plot_rose_pie(filename='epidemic_rose_pie')