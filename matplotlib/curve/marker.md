# fmt
```
fmt = '[marker][line][color]'
```
## marker
```
"."	                点
","	                像素点
"o"	                实心圆
"v"	                下三角
"^"	                上三角
"<"	                左三角
">"	                右三角
"1"	                下三叉
"2"	                上三叉
"3"	                左三叉
"4"	                右三叉
"8"	                八角形
"s"	                正方形
"p"	                五边形
"P"	                加号（填充）
"*"	                星号
"h"	                六边形 1
"H"	                六边形 2
"+"	                加号
"x"	                乘号 x
"X"	                乘号 x (填充)
"D"	                菱形
"d"	                瘦菱形
"|"	                竖线
"_"	                横线
0 (TICKLEFT)	    左横线
1 (TICKRIGHT)	    右横线
2 (TICKUP)	        上竖线
3 (TICKDOWN)	    下竖线
4 (CARETLEFT)	    左箭头
5 (CARETRIGHT)	    右箭头
6 (CARETUP)	        上箭头
7 (CARETDOWN)	    下箭头
8 (CARETLEFTBASE)	左箭头 (中间点为基准)
9 (CARETRIGHTBASE)	右箭头 (中间点为基准)
10 (CARETUPBASE)	上箭头 (中间点为基准)
11 (CARETDOWNBASE)	下箭头 (中间点为基准)
"None", " " or ""	没有任何标记
'$...$'	            渲染指定的字符。例如 "$f$" 以字母 f 为标记。
```

## linestyle
```
'solid'(默认)	    '-'	            实线
'dotted'	        ':'	            点虚线
'dashed'	        '--'	        破折线
'dashdot'	        '-.'	        点划线
'None'	            '' 或 ' '	    不画线
```

## color
```
'r'	        红色
'g'	        绿色
'b'	        蓝色
'c'	        青色
'm'	        品红
'y'	        黄色
'k'	        黑色
'w'	        白色
```