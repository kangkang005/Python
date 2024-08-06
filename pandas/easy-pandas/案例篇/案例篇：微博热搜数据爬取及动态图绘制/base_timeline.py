# -*- coding: utf-8 -*-

"""
DateTime   : 2021/02/17 20:46
Author     : ZhangYafei
Description: 
"""
import os

import imageio
from pyecharts import options as opts
from pyecharts.charts import Bar, Timeline
from pyecharts.faker import Faker
from pyecharts.globals import CurrentConfig, ThemeType
# 导入输出图片工具
from pyecharts.render import make_snapshot
# 使用snapshot-selenium 渲染图片
from snapshot_selenium import snapshot

CurrentConfig.ONLINE_HOST = 'F:\python37\pyecharts-assets/assets/'
# CurrentConfig.ONLINE_HOST = "https://cdn.kesci.com/lib/pyecharts_assets/"


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


def plot1(out_type: str = 'html', html_path: str = None,  images_dir: str = 'images', gif_path: str = None, duration = 1):
    xaxis_data = Faker.choose()
    if out_type == 'html' and html_path:
        tl = Timeline(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        for i in range(2015, 2021):
            bar = (
                Bar()
                    .add_xaxis(xaxis_data)
                    .add_yaxis("商家A", Faker.values())
                    .add_yaxis("商家B", Faker.values())
                    .set_global_opts(title_opts=opts.TitleOpts("商店{}年商品销售额".format(i)))
            )
            tl.add(bar, "{}年".format(i))
        # 输出html
        tl.render(html_path)
        print('')
    elif out_type == 'gif' and gif_path:
        image_list = []
        for i in range(2015, 2021):
            bar = (
                Bar(init_opts=opts.InitOpts(bg_color='white'))
                    .add_xaxis(xaxis_data)
                    .add_yaxis("商家A", Faker.values())
                    .add_yaxis("商家B", Faker.values())
                    .set_global_opts(title_opts=opts.TitleOpts("商店{}年商品销售额".format(i)))
            )
            make_snapshot(snapshot, bar.render(), f"{images_dir}/{i}年.png")
            image_list.append(f'{images_dir}/{i}年.png')
            print(f'{images_dir}{i}年.png 保存成功.')
        create_gif(image_list, gif_path, duration)
        print(f'{gif_path} 完成创建.')


def plot2(out_type: str = 'html', html_path: str = None, images_dir: str = 'images', gif_path: str = None, duration = 1):
    xaxis_data = Faker.choose()
    if out_type == 'html' and html_path:
        tl = Timeline(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        for i in range(2015, 2021):
            bar = (
                Bar()
                    .add_xaxis(xaxis_data)
                    .add_yaxis("商家A", Faker.values(), label_opts=opts.LabelOpts(position="right"))
                    .add_yaxis("商家B", Faker.values(), label_opts=opts.LabelOpts(position="right"))
                    .reversal_axis()
                    .set_global_opts(
                    title_opts=opts.TitleOpts("Timeline-Bar-Reversal (时间: {} 年)".format(i))
                )
            )
            tl.add(bar, "{}年".format(i))
        # 输出html
        tl.render(html_path)
        print('')
    elif out_type == 'gif' and gif_path:
        image_list = []
        for i in range(2015, 2021):
            bar = (
                Bar(init_opts=opts.InitOpts(bg_color='white'))
                    .add_xaxis(xaxis_data)
                    .add_yaxis("商家A", Faker.values(), label_opts=opts.LabelOpts(position="right"))
                    .add_yaxis("商家B", Faker.values(), label_opts=opts.LabelOpts(position="right"))
                    .reversal_axis()
                    .set_global_opts(
                    title_opts=opts.TitleOpts("Timeline-Bar-Reversal (时间: {} 年)".format(i))
                )
            )
            make_snapshot(snapshot, bar.render(), f"{images_dir}/{i}年.png")
            image_list.append(f'{images_dir}/{i}年.png')
            print(f'{images_dir}{i}年.png 保存成功.')
        create_gif(image_list, gif_path, duration)
        print(f'{gif_path} 完成创建.')


if __name__ == '__main__':
    plot1(html_path='timeline_bar.html')
    plot2(html_path='timeline_bar_reversal.html')
    # plot1(out_type='gif', images_dir='images', gif_path='timeline_bar.gif')
    # plot2(out_type='gif', images_dir='images', gif_path='timeline_bar_reversal.gif')
