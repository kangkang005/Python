# -*- coding: utf-8 -*-

"""
DateTime   : 2021/02/17 19:34
Author     : ZhangYafei
Description: 
"""
import logging
from datetime import datetime
import pandas as pd
import schedule
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


def get_content(to_file):
    print(to_file)
    logging.info('start downloading weibo hot data...')
    url = 'https://s.weibo.com/top/summary'
    df = pd.read_html(url)[0][1:11][['序号', '关键词']]  # 获取热搜前10
    time_ = datetime.now().strftime("%Y/%m/%d %H:%M")  # 获取当前时间
    df['序号'] = df['序号'].apply(int)
    df['热度'] = df['关键词'].str.split('  ', expand=True)[1]
    df['关键词'] = df['关键词'].str.split('  ', expand=True)[0]
    df['时间'] = [time_] * len(df['序号'])
    if not os.path.exists(to_file):
        df.to_csv(to_file, mode='a+', index=False)
    else:
        df.to_csv(to_file, mode='w', index=False, header=False)
    logging.info('weibo hot data downloaded, saved to data/weibo_hot.csv...')


# 定时爬虫
schedule.every(1).minutes.do(get_content, ('data/weibo_hot.csv', ))

while True:
    schedule.run_pending()
