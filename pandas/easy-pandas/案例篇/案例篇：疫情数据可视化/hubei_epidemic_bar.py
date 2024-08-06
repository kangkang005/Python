# -*- coding: utf-8 -*-

"""
DateTime   : 2021/02/18 11:17
Author     : ZhangYafei
Description: 
"""
import datetime
import logging

import requests
from pyecharts import options as opts
from pyecharts.charts import Bar
# 导入输出图片工具
from pyecharts.render import make_snapshot
# 使用snapshot-selenium 渲染图片
from snapshot_selenium import snapshot

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


def plot_hubei_bar(out_type: str = 'html', filename: str = 'hubei_epidemic_bar'):
    url = 'https://lab.isaaclin.cn/nCoV/api/area'
    data = requests.get(url).json()
    logging.info('get response success, processing data...')
    hb_data = {}
    for item in data['results']:
        if item['provinceShortName'] == '湖北':
            hb_data = item['cities']
    logging.info('data processing completed, ready to draw...')
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    hb_bar = (
        Bar(init_opts=opts.InitOpts(theme='dark'))
            .add_xaxis([hd['cityName'] for hd in hb_data])
            .add_yaxis('累计确诊人数', [hd['confirmedCount'] for hd in hb_data])
            .add_yaxis('累计治愈人数', [hd['curedCount'] for hd in hb_data])
            .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="湖北新冠疫情确诊及治愈情况", subtitle=f'截止 {date}',
                                      title_textstyle_opts=opts.TextStyleOpts(font_size=15),
                                      subtitle_textstyle_opts=opts.TextStyleOpts(font_size=12)),
            legend_opts=opts.LegendOpts(is_show=True)
        )
    )
    if out_type == 'html':
        hb_bar.render(f'{filename}.html')
    else:
        make_snapshot(snapshot, hb_bar.render(f'{filename}.html'), f'{filename}.{out_type}')
    logging.info(f'{filename}.{out_type} saved success...')


if __name__ == '__main__':
    # plot_hubei_bar()
    plot_hubei_bar(out_type='png')
