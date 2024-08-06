# -*- coding: utf-8 -*-

"""
DateTime   : 2021/02/18 17:03
Author     : ZhangYafei
Description: 
"""
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot


def bar_chart1():
    # V1 版本开始支持链式调用
    bar = (
        Bar()
        .add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
        .add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
        .set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况"))
    )
    bar.render()

    # 不习惯链式调用的开发者依旧可以单独调用方法
    # bar = Bar()
    # bar.add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
    # bar.add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
    # bar.add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
    # bar.set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况"))
    # bar.render()


def bar_chart2() -> Bar:
    bar = (
        Bar()
            .add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
            .add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
            .add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
            .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))
            .set_global_opts(title_opts=opts.TitleOpts(title="Bar-测试渲染图片"))
    )
    return bar


if __name__ == '__main__':
    # bar_chart1()
    # 需要安装 snapshot-selenium 或者 snapshot-phantomjs
    make_snapshot(snapshot, bar_chart2().render(), "bar.png")
