# -*- coding: utf-8 -*-

"""
DateTime   : 2021/02/18 17:48
Author     : ZhangYafei
Description: 
"""
import jieba
from stylecloud import gen_stylecloud


def cloud1(file_name):
    with open(file_name, 'r', encoding='utf8') as f:
        word_list = jieba.cut(f.read())
        result = " ".join(word_list)  # 分词用 隔开
        # 制作中文云词
        gen_stylecloud(text=result,
                       font_path='C:\\Windows\\Fonts\\simhei.ttf',
                       output_name='t1.png',
                       )  # 必须加中文字体，否则格式错误


def cloud2(file_name):
    with open(file_name, 'r', encoding='utf8') as f:
        word_list = jieba.cut(f.read())
        result = " ".join(word_list)  # 分词用 隔开
        # 制作中文云词
        gen_stylecloud(text=result,
                       font_path='C:\\Windows\\Fonts\\simhei.ttf',
                       background_color='black',
                       output_name='t2.png',
                       )  # 必须加中文字体，否则格式错误

def cloud3(file_name):
    with open(file_name,'r',encoding='utf8') as f:
        word_list = jieba.cut(f.read())
        result = " ".join(word_list) #分词用 隔开
        #制作中文云词
        gen_stylecloud(text=result,
                       font_path='C:\\Windows\\Fonts\\simhei.ttf',
                       background_color= 'black',
                       #palette='cartocolors.diverging.ArmyRose_3',
                       palette='colorbrewer.diverging.Spectral_11',
                       output_name='t3.png',
                       ) #必须加中文字体，否则格式错误


def cloud4(file_name):
    with open(file_name,'r',encoding='utf8') as f:
        word_list = jieba.cut(f.read())
        result = " ".join(word_list) #分词用 隔开
        #制作中文云词
        gen_stylecloud(text=result,
                       font_path='C:\\Windows\\Fonts\\simhei.ttf',
                       # background_color= 'black',
                       palette='cartocolors.diverging.Fall_4',
                       icon_name='fas fa-plane',
                       output_name='t4.png',
                       ) #必须加中文字体，否则格式错误

def cloud5(file_name):
    with open(file_name,'r',encoding='utf8') as f:
        word_list = jieba.cut(f.read())
        result = " ".join(word_list) #分词用 隔开
        #制作中文云词
        gen_stylecloud(text=result,
                       font_path='C:\\Windows\\Fonts\\simhei.ttf',
                       # background_color= 'black',
                       palette='cartocolors.diverging.TealRose_2',
                       icon_name='fas fa-bell',
                       gradient='vertical' ,
                       output_name='t5.png',
                       ) #必须加中文字体，否则格式错误

if __name__ == "__main__":
    file_name = 'word.txt'
    # cloud1(file_name)
    # cloud2(file_name)
    # cloud3(file_name)
    # cloud4(file_name)
    cloud5(file_name)