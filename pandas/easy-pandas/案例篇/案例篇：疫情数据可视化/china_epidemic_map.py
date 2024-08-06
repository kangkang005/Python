# -*- coding: utf-8 -*-

"""
DateTime   : 2021/02/18 11:09
Author     : ZhangYafei
Description: 
"""
import datetime
import logging

import requests
from pyecharts import options as opts
from pyecharts.charts import Map
# 导入输出图片工具
from pyecharts.render import make_snapshot
# 使用snapshot-selenium 渲染图片
from snapshot_selenium import snapshot

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


def plot_china_map(out_type: str = 'html', filename: str = 'china_epidemic_map'):
    url = 'https://lab.isaaclin.cn/nCoV/api/area'
    data = requests.get(url).json()
    logging.info('get response success, processing data...')
    province_data = []
    for item in data['results']:
        if item['countryName'] == '中国':
            province_data.append((item['provinceShortName'], item['confirmedCount']))

    logging.info('data processing completed, ready to draw...')
    date = datetime.datetime.now().strftime('%Y-%m-%d')

    china_map = (
        Map(init_opts=opts.InitOpts(theme='dark'))
            .add('确诊人数', province_data, 'china', is_map_symbol_show=False, is_roam=False)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True, color='#ffffff'))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="中国疫情累计确诊人数地图", subtitle=f'截止 {date}',
                                      title_textstyle_opts=opts.TextStyleOpts(font_size=15),
                                      subtitle_textstyle_opts=opts.TextStyleOpts(font_size=12)),
            legend_opts=opts.LegendOpts(is_show=False),
            visualmap_opts=opts.VisualMapOpts(max_=2000,
                                              is_piecewise=True,
                                              pieces=[
                                                  {"max": 99999, "min": 10000, "label": "10000人及以上", "color": "#8A0808"},
                                                  {"max": 9999, "min": 1000, "label": "1000-9999人", "color": "#B40404"},
                                                  {"max": 999, "min": 500, "label": "500-999人", "color": "#DF0101"},
                                                  {"max": 499, "min": 100, "label": "100-499人", "color": "#F78181"},
                                                  {"max": 99, "min": 10, "label": "10-99人", "color": "#F5A9A9"},
                                                  {"max": 9, "min": 0, "label": "1-9人", "color": "#FFFFCC"},
                                              ])
        )
    )
    if out_type == 'html':
        china_map.render(f'{filename}.html')
    else:
        make_snapshot(snapshot, china_map.render(f'{filename}.html'), f'{filename}.{out_type}')
    logging.info(f'{filename}.{out_type} saved success...')


if __name__ == '__main__':
    # plot_china_map()
    plot_china_map(out_type='png')
