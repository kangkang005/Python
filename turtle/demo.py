from turtle import *
'''
@Canvas:
    turtle.setup(宽度, 高度) - 设置画布的宽度和高度
    turtle.title(标题) - 设置标题

@Move:
    turtle.forward(距离) / turtle.fd(距离) - 控制笔前进指定距离
    turtle.back(距离)/turtle.bk(距离) - 控制笔后退指定距离
    turtle.goto(x坐标, y坐标)/ turtle.setx(x坐标) / turtle.sety(y坐标) - 控制笔移动到指定位置（坐标原点在画布的中心）
    turtle.home() - 笔回到初始状态（回到初始位置和初始方向）

@Direction:
    turtle.left(角度) - 向左旋转指定角度
    turtle.right(角度) - 向右旋转指定角度
    turtle.setheading(角度) - 设置绝对角度值指定度数

@Pencil:
    turtle.pencolor(颜色) - 设置画笔画出的线的颜色
    turtle.width(线宽) - 设置线宽
    turtle.speed(速度值) - 设置笔移动的速度 (速度值是 1-10 逐渐变快；0 对应的速度最慢）

@Fill:
    turtle.fillcolor(颜色) - 设置填充颜色
    turtle.begin_fill() - 开始填充
    turtle.end_fill() - 结束填充
'''
pencolor = [
    "red",
    "blue",
    "green",
    "purple"
]
t = Turtle()
# canvas setup
setup(800, 600)
title('hello')

# pen property
t.pencolor("red")
t.width(2)

# fill property
t.fillcolor('orange')
t.begin_fill()

# draw square
for i in range(4):
    t.pencolor(pencolor[i])
    t.forward(100)
    t.left(90)

t.end_fill()

# hide arrow
t.hideturtle()
done()