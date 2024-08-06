from turtle import *

t = Turtle()

def draw_spiral(t, line_len):
    if line_len <= 0:
        return
    t.forward(line_len)
    t.right(90)
    draw_spiral(t, line_len-5)

def draw_tree(t):
    def tree(t, branch_len):
        if branch_len <= 5:
            return
        t.forward(branch_len)
        t.right(20)
        tree(t, branch_len - 15)    # right branch
        t.left(40)
        tree(t, branch_len - 15)    # left branch
        t.right(20)
        t.backward(branch_len)
    t.left(90)
    t.penup()
    t.backward(100)
    t.pendown()
    t.pencolor("green")
    t.pensize(2)
    tree(t, 75)

# draw_spiral(t, 100)
draw_tree(t)
done()