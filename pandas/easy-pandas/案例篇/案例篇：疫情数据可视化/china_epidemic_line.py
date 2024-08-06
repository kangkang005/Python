# -*- coding: utf-8 -*-

"""
DateTime   : 2021/02/18 11:29
Author     : ZhangYafei
Description: 
"""
import logging

import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Line
# 导入输出图片工具
from pyecharts.render import make_snapshot
# 使用snapshot-selenium 渲染图片
from snapshot_selenium import snapshot

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


def plot_china_line(out_type: str = 'html', filename: str = 'china_epidemic_line'):
    df = pd.read_excel('data/china_history.xlsx', index_col='date', date_parser='date')
    df = df.resample('15d').max()
    date = df.index.strftime('%Y-%m-%d').to_list()
    confirm = df['confirm'].to_list()
    heal = df['heal'].to_list()

    logging.info('data read completed, ready to draw...')
    line = (Line(init_opts=opts.InitOpts(bg_color='white'))
        .add_xaxis(date)
        .add_yaxis('累计确诊', confirm, color='#10aeb5')
        .add_yaxis('累计治愈', heal, color='#e83132')
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
        .set_global_opts(
        title_opts=opts.TitleOpts(title='中国疫情随时间变化趋势')
    ))
    if out_type == 'html':
        line.render(f'{filename}.html')
    else:
        make_snapshot(snapshot, line.render(f'{filename}.html'), f'{filename}.{out_type}')
    logging.info(f'{filename}.{out_type} saved success...')


if __name__ == '__main__':
    plot_china_line(out_type='png')
