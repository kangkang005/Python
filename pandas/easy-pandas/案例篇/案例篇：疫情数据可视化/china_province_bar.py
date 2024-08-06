# -*- coding: utf-8 -*-

"""
DateTime   : 2021/02/21 18:30
Author     : ZhangYafei
Description: 
"""

import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Timeline, Grid
from pyecharts.globals import ThemeType, CurrentConfig

# CurrentConfig.ONLINE_HOST = 'F:\python37\pyecharts-assets/assets/'
CurrentConfig.ONLINE_HOST = "https://cdn.kesci.com/lib/pyecharts_assets/"


def country_data_convert(name_col: str, date_col: str, confirm_col: str, to_file: str):
    """
    世界各国数据转换 ->
    :param name_col: 国家名称列
    :param date_col: 时间列
    :param confirm_col: 确诊人数列
    :param to_file: 生成文件路径
    :return:
    """
    df = pd.read_csv('data/country_data.csv', parse_dates=[date_col])
    df[date_col] = df[date_col].dt.strftime('%Y-%m-%d')
    date_list = df[date_col].unique()
    date_list.sort()
    name_list = [name for name in df[name_col].unique() if pd.notna(name)]

    df.set_index([date_col, name_col], inplace=True)

    data = pd.DataFrame(index=name_list, columns=date_list)

    for date in date_list:
        for name in df.loc[date, :].index:
            data.loc[name, date] = int(df.loc[(date, name), confirm_col])

    data.index.name = name_col
    data.fillna(0, inplace=True)
    data.to_excel(to_file)


def plot(file: str, name_col: str, title: str, num: int = 10, duration=1.0, html_path: str = 'render.html'):
    df = pd.read_excel(file, index_col=name_col)
    date_list = df.columns.to_list()

    t = Timeline(init_opts=opts.InitOpts(theme=ThemeType.MACARONS))  # 定制主题
    for date in date_list:
        data = df.sort_values(date, ascending=False)[:num][::-1]

        x = data.index.to_list()
        y = data[date].to_list()

        bar = (
            Bar()
                .add_xaxis(x)  # x轴数据
                .add_yaxis('确诊人数', y)  # y轴数据
                .reversal_axis()  # 翻转
                .set_global_opts(  # 全局配置项
                title_opts=opts.TitleOpts(  # 标题配置项
                    title=f'{title}(日期：{date})',
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
            play_interval=duration * 1000,  # 轮播速度
            is_timeline_show=True,  # 是否显示 timeline 组件
            is_auto_play=False,  # 是否自动播放
        )

    t.render(html_path)


if __name__ == '__main__':
    plot(html_path='各省份每日确诊人数动态图.html', file='data/covid19_province_data.xlsx.xlsx', name_col='省级行政区',
         title='全国各省市新冠数据', duration=0.3)
    # country_data_convert(name_col='countryName', date_col='dateId', confirm_col='confirmedCount',
    #                      to_file='data/covid19_country_data.xlsx')
    # plot(html_path='世界各国新冠疫情数据动态图.html', file='data/covid19_country_data.xlsx', name_col='countryName', title='世界各国新冠数据', duration=0.3)
