# -*- coding: utf-8 -*-

"""
DateTime   : 2021/02/17 20:09
Author     : ZhangYafei
Description: 
"""
import os

import imageio
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Timeline, Grid
from pyecharts.globals import ThemeType, CurrentConfig
# 导入输出图片工具
from pyecharts.render import make_snapshot
# 使用snapshot-selenium 渲染图片
from snapshot_selenium import snapshot


CurrentConfig.ONLINE_HOST = 'F:\python37\pyecharts-assets/assets/'


def create_gif(image_list, gif_path, duration=1.0):
    """
    :param image_list: 这个列表用于存放生成动图的图片
    :param gif_path: 字符串，所生成gif文件名，带.gif后缀
    :param duration: 图像间隔时间
    :return:
    """
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))

    imageio.mimsave(gif_path, frames, 'GIF', duration=duration)


def plot(out_type: str = 'html', html_path: str = None, images_dir: str = 'images', gif_path: str = None, duration=1):
    df = pd.read_csv('data/weibo_hot.csv')
    if out_type == 'html' and html_path:
        t = Timeline(init_opts=opts.InitOpts(theme=ThemeType.MACARONS))  # 定制主题
        for i in range(df.shape[0] // 10):
            bar = (
                Bar()
                    .add_xaxis(list(df['关键词'][i * 10: i * 10 + 10][::-1]))  # x轴数据
                    .add_yaxis('热度', list(df['热度'][i * 10: i * 10 + 10][::-1]))  # y轴数据
                    .reversal_axis()  # 翻转
                    .set_global_opts(  # 全局配置项
                    title_opts=opts.TitleOpts(  # 标题配置项
                        title=f"{list(df['时间'])[i * 10]}",
                        pos_right="5%", pos_bottom="15%",
                        title_textstyle_opts=opts.TextStyleOpts(
                            font_family='KaiTi', font_size=24, color='#FF1493'
                        )
                    ),
                    xaxis_opts=opts.AxisOpts(  # x轴配置项
                        splitline_opts=opts.SplitLineOpts(is_show=True),
                    ),
                    yaxis_opts=opts.AxisOpts(  # y轴配置项
                        splitline_opts=opts.SplitLineOpts(is_show=True),
                        axislabel_opts=opts.LabelOpts(color='#DC143C')
                    )
                )
                    .set_series_opts(  # 系列配置项
                    label_opts=opts.LabelOpts(  # 标签配置
                        position="right", color='#9400D3')
                )
            )
            grid = (
                Grid()
                    .add(bar, grid_opts=opts.GridOpts(pos_left="24%"))
            )
            t.add(grid, "")
            t.add_schema(
                play_interval=100,  # 轮播速度
                is_timeline_show=False,  # 是否显示 timeline 组件
                is_auto_play=True,  # 是否自动播放
            )

        t.render(html_path)
    elif out_type == 'gif' and images_dir:
        image_list = []
        for i in range(df.shape[0] // 10):
            title = f"{list(df['时间'])[i * 10]}"
            bar = (
                Bar(init_opts=opts.InitOpts(bg_color='white'))
                    .add_xaxis(list(df['关键词'][i * 10: i * 10 + 10][::-1]))  # x轴数据
                    .add_yaxis('热度', list(df['热度'][i * 10: i * 10 + 10][::-1]))  # y轴数据
                    .reversal_axis()  # 翻转
                    .set_global_opts(  # 全局配置项
                    title_opts=opts.TitleOpts(  # 标题配置项
                        title=title,
                        pos_right="5%", pos_bottom="15%",
                        title_textstyle_opts=opts.TextStyleOpts(
                            font_family='KaiTi', font_size=24, color='#FF1493'
                        )
                    ),
                    xaxis_opts=opts.AxisOpts(  # x轴配置项
                        splitline_opts=opts.SplitLineOpts(is_show=True),
                    ),
                    yaxis_opts=opts.AxisOpts(  # y轴配置项
                        splitline_opts=opts.SplitLineOpts(is_show=True),
                        axislabel_opts=opts.LabelOpts(color='#DC143C')
                    )
                )
                    .set_series_opts(  # 系列配置项
                    label_opts=opts.LabelOpts(  # 标签配置
                        position="right", color='#9400D3')
                )
            )
            grid = (
                Grid(init_opts=opts.InitOpts(bg_color='white'))
                    .add(bar, grid_opts=opts.GridOpts(pos_left="24%"))
            )
            make_snapshot(snapshot, grid.render(), f"{images_dir}/{i}.png")
            image_list.append(f"{images_dir}/{i}.png")
            print(f'{images_dir}{i}.png 保存成功.')
        create_gif(image_list, gif_path, duration)
        print(f'{gif_path} 完成创建.')


if __name__ == '__main__':
    plot(html_path='微博热搜动态图.html')
    # plot(out_type='gif', gif_path='微博热搜动态图.gif', duration=1)
