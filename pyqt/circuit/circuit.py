import math
import copy
import numpy as np

from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtCore import QLine


class GraphicScene(QGraphicsScene):

    def __init__(self, parent=None):
        super().__init__(parent)

        # 禁用索引的快速查询, 防止删除item后场景还有残余的item
        self.setItemIndexMethod(QGraphicsScene.NoIndex)

        # 一些关于网格背景的设置
        self.grid_size = 20  # 一块网格的大小 （正方形的）, 最小网格单元的大小
        self.grid_squares = 5  # 网格中正方形的区域个数
        self.nodes = []  # 存储图元
        self.edges = []  # 存储连线

		# 一些颜色
        self._color_background = QColor('#393939')
        self._color_light = QColor('#2f2f2f')
        self._color_dark = QColor('#292929')
		# 一些画笔
        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)

		# 设置画背景的画笔
        self.setBackgroundBrush(self._color_background)
        self.setSceneRect(0, 0, 500, 500)

	# override
    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

		# 获取背景矩形的上下左右的长度，分别向上或向下取整数
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

		# 从左边和上边开始
        first_left = left - (left % self.grid_size)  # 减去余数，保证可以被网格大小整除
        first_top = top - (top % self.grid_size)

		# 分别收集明、暗线
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.grid_size):
            if x % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.grid_size):
            if y % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))

		# 最后把收集的明、暗线分别画出来
        painter.setPen(self._pen_light)
        if lines_light:
            painter.drawLines(*lines_light)

        painter.setPen(self._pen_dark)
        if lines_dark:
            painter.drawLines(*lines_dark)

    def add_node(self, node):
        self.nodes.append(node)
        self.addItem(node)

    def remove_node(self, node):
        self.nodes.remove(node)
        # 删除图元时，遍历与其连接的线，并移除
        # for edge in self.edges:
        #     if edge.edge_wrap.start_item is node or edge.edge_wrap.end_item is node:
        #         self.remove_edge(edge)
        if isinstance(node, GraphicItemGroup):
            for child_item in node.childItems():
                if child_item.component == Terminal:
                    for edge in child_item.edges:
                        self.remove_edge(edge)
                    child_item.clear_edge()
        self.removeItem(node)

    def add_edge(self, edge):
        self.edges.append(edge)
        self.addItem(edge)

    def remove_edge(self, edge):
        self.edges.remove(edge)
        self.removeItem(edge)

from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtGui import QPainter

class GraphicView(QGraphicsView):

    def __init__(self, graphic_scene, parent=None):
        super().__init__(parent)
        self.gr_scene = graphic_scene  # 将scene传入此处托管，方便在view中维护
        self.parent = parent

        self.edge_enable = False  # 用来记录目前是否可以画线条
        self.drag_edge = None  # 记录拖拽时的线

        self.init_ui()

    def init_ui(self):
        self.setScene(self.gr_scene)
        # 设置渲染属性
        self.setRenderHints(QPainter.Antialiasing |                    # 抗锯齿
                            QPainter.HighQualityAntialiasing |         # 高品质抗锯齿
                            QPainter.TextAntialiasing |                # 文字抗锯齿
                            QPainter.SmoothPixmapTransform |           # 使图元变换更加平滑
                            QPainter.LosslessImageRendering)           # 不失真的图片渲染
        # 视窗更新模式
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        # 设置水平和竖直方向的滚动条不显示
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(self.AnchorUnderMouse)
        # 设置拖拽模式
        self.setDragMode(self.RubberBandDrag)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        # 当按下键盘E键时，启动线条功能，再次按下则是关闭
        if event.key() == Qt.Key_E:
            self.edge_enable = ~self.edge_enable
            if self.edge_enable:
                print("Put Line")
        elif event.key() == Qt.Key_R:
            # TODO: if select more than device
            print("Rotation")
            selected_items = self.gr_scene.selectedItems()
            for selected_item in selected_items:
                selected_item.setRotation(selected_item.rotation()+90)
                if isinstance(selected_item, GraphicItemGroup):
                    for child_item in selected_item.childItems():
                        if child_item.component == Terminal:
                            for gr_edge in child_item.edges:
                                gr_edge.edge_wrap.update_positions()

    def mousePressEvent(self, event):
        item = self.get_item_at_click(event)
        if event.button() == Qt.RightButton:   # 判断鼠标右键点击
            if isinstance(item, GraphicItem):  # 判断点击对象是否为图元的实例
                group = item.group()
                if group:
                    self.gr_scene.remove_node(group)
                else:
                    self.gr_scene.remove_node(item)
        elif self.edge_enable:
            if isinstance(item, GraphicItem):
                group = item.group()
                if not group or (group and item.component == Terminal):
                    # 确认起点是图元后，开始拖拽
                    self.edge_drag_start(item)
            elif isinstance(item, Point):
                self.edge_drag_start(item)
        else:
            if event.button() == Qt.LeftButton:
                if isinstance(item, GraphicItem):
                    pass
                    # print(item.component)
        	# 如果写到最开头，则线条拖拽功能会不起作用
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.edge_enable:
        	# 拖拽结束后，关闭此功能
            self.edge_enable = False
            if self.drag_edge:
                self.drag_edge.remove()
                self.drag_edge = None
            item = self.get_item_at_click(event)
            # 终点图元不能是起点图元，即无环图
            if isinstance(item, GraphicItem):
                group = item.group()
                if not group or (group and item.component == Terminal):
                    if self.drag_start_item and item is not self.drag_start_item:
                        self.edge_drag_end(item)
            elif item is None:
                pos = event.pos()
                item = Point()
                item.setPos(pos)
                self.gr_scene.add_node(item)
                if self.drag_start_item and item is not self.drag_start_item:
                    self.edge_drag_end(item)
        else:
            self.update_selected()
            super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
    	# 实时更新线条
        pos = event.pos()
        if self.edge_enable and self.drag_edge is not None:
            sc_pos = self.mapToScene(pos)
            self.drag_edge.gr_edge.set_dst(sc_pos.x(), sc_pos.y())
            self.drag_edge.gr_edge.update()
        super().mouseMoveEvent(event)
        # 如果图元被选中，就更新连线，这里更新的是所有。可以优化，只更新连接在图元上的。

    def get_item_at_click(self, event):
        """ 获取点击位置的图元，无则返回None. """
        pos = event.pos()
        item = self.itemAt(pos)
        return item

    def get_items_at_rubber_select(self):
        area = self.rubberBandRect()
        return self.items(area)   # 返回一个所有选中图元的列表，对此操作即可

    def edge_drag_start(self, item):
        self.drag_start_item = item  # 拖拽开始时的图元，此属性可以不在__init__中声明
        self.drag_edge = Edge(self.gr_scene, self.drag_start_item, None)  # 开始拖拽线条，注意到拖拽终点为None

    def edge_drag_end(self, item):
        # self.drag_edge.remove()  # 删除拖拽时画的线
        # self.drag_edge = None
        new_edge = Edge(self.gr_scene, self.drag_start_item, item)  # 拖拽结束
        # new_edge.store()  # 保存最终产生的连接线

    # TODO
    def update_selected(self):
        selected_items = self.gr_scene.selectedItems()
        for selected_item in selected_items:
            if not isinstance(selected_item, GraphicItemGroup):
                continue


from PyQt5.QtWidgets import QGraphicsItem, QGraphicsItemGroup, QGraphicsLineItem, QGraphicsPathItem
from PyQt5.QtGui import QPainterPath, QPen
from PyQt5.QtCore import QRectF

class Power(QPainterPath):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

    def draw(self):
        self.moveTo(-self.width*0.5, 0)
        self.lineTo(-10, 0)
        self.moveTo(-10, self.height*0.1)
        self.lineTo(-10, -self.height*0.1)
        self.moveTo(10, self.height*0.2)
        self.lineTo(10, -self.height*0.2)
        self.moveTo(10, 0)
        self.lineTo(self.width*0.5, 0)

class Voltage(QPainterPath):
    def __init__(self, width, height):
        super().__init__()
        self.width = width*0.5*1/3
        self.height = height*0.5*1/3
        self.name = "Voltage"
        self.coords = [
            [[-0.25, 0.50], [0.25, 0.50]],
            [[0.00, 3.00], [0.00, 1.00]],
            [[0.00, -0.75], [0.00, -0.25]],
            [[0.00, -1.00], [0.00, -3.00]],
            [[-0.25, -0.50], [0.25, -0.50]],
            [[-1.00, -1.00, 2.00, 2.00]],
        ]
        self.terminals = {
            "p" : [self.width*self.coords[3][1][0], self.height*self.coords[3][1][1]],
            "n" : [self.width*self.coords[1][0][0], self.height*self.coords[1][0][1]],
        }
        self.direction = {
            "p" : [0, -1],
            "n" : [0, 1],
        }

    def draw(self):
        for coord in self.coords:
            begin = coord[0]
            if len(begin) == 2:
                self.moveTo(self.width*begin[0], self.height*begin[1])
                for end in coord[1:]:
                    self.lineTo(self.width*end[0], self.height*end[1])
            elif len(begin) == 4:
                self.addEllipse(self.width*begin[0], self.height*begin[1], self.width*begin[2], self.height*begin[3])

    def get_terminal(self):
        return self.terminals


class GND(QPainterPath):
    def __init__(self, width, height):
        super().__init__()
        # last 0.5 is factor for zoom in
        self.width = width*0.5*1/1*0.5
        self.height = height*0.5*1/2*0.5
        self.name = "GND"
        self.coords = [
            [[0., -2.], [0., 1.]],
            [[0., 2.], [1., 1.], [-1., 1.], [0., 2.]],
        ]
        self.terminals = {
            "gnd" : [self.width*self.coords[0][0][0], self.height*self.coords[0][0][1]],
        }
        self.direction = {
            "gnd" : [0, -1],
        }

    def draw(self):
        for coord in self.coords:
            begin = coord[0]
            self.moveTo(self.width*begin[0], self.height*begin[1])
            for end in coord[1:]:
                self.lineTo(self.width*end[0], self.height*end[1])

    def get_terminal(self):
        return self.terminals

class NMOS(QPainterPath):
    def __init__(self, width, height):
        super().__init__()
        self.width = width*0.5*1/2
        self.height = height*0.5*1/3
        self.name = "NMOS"
        self.coords = [
            [[0.00, 1.50],  [0.00, -1.50]],
            [[2.00, 3.00],  [2.00, 1.50]],
            [[2.00, -1.50], [2.00, -3.00]],
            [[0.00, -1.50], [2.00, -1.50]],
            [[2.00, 1.50],  [0.00, 1.50]],
            [[-0.50, 0.00], [-2.00, 0.00]],
            [[0.00, 0.00],  [2.00, 0.00]],
            [[-0.50, 1.50], [-0.50, -1.50]],

            [[1.00, 1.00], [2.00, 1.50]],
            [[2.00, 1.50], [1.00, 2.00]]
        ]
        self.terminals = {
            "gate" : [self.width*self.coords[5][1][0], self.height*self.coords[5][1][1]],
            "source" : [self.width*self.coords[1][0][0], self.height*self.coords[1][0][1]],
            "drain" : [self.width*self.coords[2][1][0], self.height*self.coords[2][1][1]],
            "bulk" : [self.width*self.coords[6][1][0], self.height*self.coords[6][1][1]],
        }
        self.direction = {
            "gate" : [-1, 0],
            "drain" : [0, -1],
            "source" : [0, 1],
            "bulk" : [1, 0],
        }

    def draw(self):
        for coord in self.coords:
            begin = coord[0]
            end = coord[1]
            self.moveTo(self.width*begin[0], self.height*begin[1])
            self.lineTo(self.width*end[0], self.height*end[1])

    def get_terminal(self):
        return self.terminals

class PMOS(QPainterPath):
    def __init__(self, width, height):
        super().__init__()
        self.width = width*0.5*1/2
        self.height = height*0.5*1/3
        self.name = "PMOS"
        self.coords = [
            [[0.00, 1.50],  [0.00, -1.50]],
            [[2.00, 3.00],  [2.00, 1.50]],
            [[2.00, -1.50], [2.00, -3.00]],
            [[0.00, -1.50], [2.00, -1.50]],
            [[2.00, 1.50],  [0.00, 1.50]],
            [[-0.50, 0.00], [-2.00, 0.00]],
            [[0.00, 0.00],  [2.00, 0.00]],
            [[-0.50, 1.50], [-0.50, -1.50]],

            [[1.00, -2.00],  [0.00, -1.50]],
            [[1.00, -1.00],  [0.00, -1.50]]
        ]
        self.terminals = {
            "gate" : [self.width*self.coords[5][1][0], self.height*self.coords[5][1][1]],
            "drain" : [self.width*self.coords[1][0][0], self.height*self.coords[1][0][1]],
            "source" : [self.width*self.coords[2][1][0], self.height*self.coords[2][1][1]],
            "bulk" : [self.width*self.coords[6][1][0], self.height*self.coords[6][1][1]],
        }
        self.direction = {
            "gate" : [-1, 0],
            "drain" : [0, 1],
            "source" : [0, -1],
            "bulk" : [1, 0],
        }

    def draw(self):
        for coord in self.coords:
            begin = coord[0]
            end = coord[1]
            self.moveTo(self.width*begin[0], self.height*begin[1])
            self.lineTo(self.width*end[0], self.height*end[1])

    def get_terminal(self):
        return self.terminals

class NPN(QPainterPath):
    def __init__(self, width, height):
        super().__init__()
        self.width = width*0.5*1/2
        self.height = height*0.5*1/3
        self.name = "NPN"
        self.coords = [
            [[0.00, 0.75], [2.00, 1.50]],
            [[0.00, 1.50], [0.00, -1.50]],
            [[2.00, 1.50], [2.00, 3.00]],
            [[0.00, 0.00], [-2.00, 0.00]],
            [[2.00, -1.50], [2.00, -3.00]],
            [[0.00, -0.75], [2.00, -1.50]],

            [[2.00, 1.50], [1.50, 0.75]],
            [[2.00, 1.50], [1.25, 1.75]],
        ]

    def draw(self):
        for coord in self.coords:
            begin = coord[0]
            end = coord[1]
            self.moveTo(self.width*begin[0], self.height*begin[1])
            self.lineTo(self.width*end[0], self.height*end[1])

class PNP(QPainterPath):
    def __init__(self, width, height):
        super().__init__()
        self.width = width*0.5*1/2
        self.height = height*0.5*1/3
        self.name = "NPN"
        self.coords = [
            [[0.00, 0.75], [2.00, 1.50]],
            [[0.00, 1.50], [0.00, -1.50]],
            [[2.00, 1.50], [2.00, 3.00]],
            [[0.00, 0.00], [-2.00, 0.00]],
            [[2.00, -1.50], [2.00, -3.00]],
            [[0.00, -0.75], [2.00, -1.50]],

            [[1.00, -1.00], [1.75, -0.75]],
            [[1.00, -1.00], [1.25, -1.75]],
        ]

    def draw(self):
        for coord in self.coords:
            begin = coord[0]
            end = coord[1]
            self.moveTo(self.width*begin[0], self.height*begin[1])
            self.lineTo(self.width*end[0], self.height*end[1])

class Terminal(QPainterPath):
    def __init__(self, width, height):
        super().__init__()
        self.width = width*0.5
        self.height = height*0.5
        self.name = "Terminal"

    def draw(self):
        self.addRect(-self.width, -self.height, self.width*2, self.height*2)

class GraphicItem(QGraphicsItem):
    def __init__(self, component, *, width=80, height=80, parent=None):
        super().__init__(parent)
        self.component = component
        self.width = width         # 图元宽
        self.height = height        # 图元高
        self.color = "#7CFC00"
        self.fill_color = "red"
        self.setFlag(QGraphicsItem.ItemIsSelectable)  # ***设置图元是可以被选择的
        self.setFlag(QGraphicsItem.ItemIsMovable)     # ***设置图元是可以被移动的

        self.path = self.component(self.width, self.height)
        if type(self.path) == Terminal:
            self.color = self.fill_color
        self.path.draw()
        self.edges = set()

    # 必须实现的两个方法 painter 和 boundingRect
    def paint(self, painter, option, widget):
        # 绘制自己，默认是图元中心作为原点
        if type(self.path) == Terminal:
            painter.setBrush(QColor(self.fill_color))    # 设置画刷颜色-用于填充颜色
        painter.setPen(QPen(QColor(self.color), 1, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin))        # 设置画笔颜色
        painter.drawPath(self.path)    # 绘制path

    def boundingRect(self):
        rect = QRectF(-self.width/2, -self.height/2, self.width, self.height)
        return rect

    def get_terminal(self):
        return self.path.get_terminal()

    def add_edge(self, edge):
        self.edges.add(edge)

    def remove_edge(self, edge):
        self.edges.remove(edge)

    def clear_edge(self):
        self.edges = []

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # 如果图元被选中，就更新连线。
        if self.isSelected():
            for gr_edge in self.edges:
                gr_edge.edge_wrap.update_positions()

class GraphicItemGroup(QGraphicsItemGroup):
    def __init__(self, component, parent=None):
        super().__init__(parent)
        self.component = component
        self.setFlag(QGraphicsItem.ItemIsSelectable)  # ***设置图元是可以被选择的
        self.setFlag(QGraphicsItem.ItemIsMovable)     # ***设置图元是可以被移动的

        dev = GraphicItem(self.component)
        terminal = dev.get_terminal()
        self.addToGroup(dev)
        for name, coord in terminal.items():
            term = GraphicItem(Terminal, height=10, width=10)
            # TODO: direction, and rotation direction
            term.direction = dev.path.direction[name]
            self.addToGroup(term)
            term.setPos(QPointF(*coord))        # GraphicItem 在父类 GraphicItemGroup 上的坐标

    def paint(self, painter, option, widget):
        rect = self.boundingRect()
        if self.isSelected():      # 被选中时，改变方框的样式
            painter.setPen(QPen(QColor("yellow"), 1, Qt.DashLine, Qt.FlatCap, Qt.MiterJoin))        # 设置画笔颜色
            painter.drawRect(QRectF(rect.x(), rect.y(), rect.width(), rect.height()))

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # 如果图元被选中，就更新连线，这里更新的是所有。可以优化，只更新连接在图元上的。
        if self.isSelected():
            for gr_edge in self.scene().edges:
                gr_edge.edge_wrap.update_positions()

class Point(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.edges = set()

    def add_edge(self, edge):
        self.edges.add(edge)

    def remove_edge(self, edge):
        self.edges.remove(edge)

    def clear_edge(self):
        self.edges = []

    def paint(self, painter, option, widget):
        painter.setBrush(QColor("blue"))
        painter.setPen(QPen(QColor("blue")))
        painter.drawEllipse(-5, -5, 10, 10)

    def boundingRect(self):
        rect = QRectF(-10, -10, 20, 20)
        return rect

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        # 如果图元被选中，就更新连线，这里更新的是所有。可以优化，只更新连接在图元上的。
        if self.isSelected():
            for gr_edge in self.scene().edges:
                gr_edge.edge_wrap.update_positions()

class GraphicEdge(QGraphicsPathItem):
    def __init__(self, edge_wrap, parent=None):
        super().__init__(parent)
        # 这个参数是GraphicEdge的包装类，见下文
        self.edge_wrap = edge_wrap
        self.width = 3.0  # 线条的宽度
        self.pos_src = [0, 0]  # 线条起始位置 x，y坐标
        self.pos_dst = [0, 0]  # 线条结束位置

        self._pen = QPen(QColor("#000"))  # 画线条的
        self._pen.setWidthF(self.width)

        self._pen_dragging = QPen(QColor("#000"))  # 画拖拽线条时线条的
        self._pen_dragging.setStyle(Qt.DashDotLine)
        self._pen_dragging.setWidthF(self.width)

        self.setFlag(QGraphicsItem.ItemIsSelectable)  # 线条可选
        self.setZValue(-1)  # 让线条出现在所有图元的最下层

        self.direction = [1, 0]
        if hasattr(self.edge_wrap.start_item, "direction"):
            self.direction = copy.deepcopy(self.edge_wrap.start_item.direction)

    def set_src(self, x, y):
        self.pos_src = [x, y]

    def set_dst(self, x, y):
        self.pos_dst = [x, y]

	# 计算线条的路径
    def calc_path(self):
        path = QPainterPath(QPointF(self.pos_src[0], self.pos_src[1]))  # 起点
        path.lineTo(self.pos_dst[0], self.pos_dst[1])  # 终点
        return path

    def calc_path(self):
        direction = self.direction
        path = QPainterPath(QPointF(self.pos_src[0], self.pos_src[1]))  # 起点
        if ((np.sign(self.pos_dst[0]-self.pos_src[0]) + np.sign(direction[0])) == 0 and direction[1] == 0):
            path.lineTo(self.pos_src[0] + 10*direction[0], self.pos_src[1])
            path.lineTo(self.pos_src[0] + 10*direction[0], self.pos_dst[1])
            path.lineTo(self.pos_dst[0], self.pos_dst[1])  # 终点
            self.end_direction = [np.sign(self.pos_dst[0]-self.pos_src[0]), 0]
        elif ((np.sign(self.pos_dst[1]-self.pos_src[1]) + np.sign(direction[1])) == 0 and direction[0] == 0):
            path.lineTo(self.pos_src[0], self.pos_src[1] + 10*direction[1])
            path.lineTo(self.pos_dst[0], self.pos_src[1] + 10*direction[1])
            path.lineTo(self.pos_dst[0], self.pos_dst[1])  # 终点
            self.end_direction = [0, np.sign(self.pos_dst[1]-self.pos_src[1])]
        else:
            pos_mid = [self.pos_src[0] + (self.pos_dst[0]-self.pos_src[0])*abs(direction[0]), self.pos_src[1] + (self.pos_dst[1]-self.pos_src[1])*abs(direction[1])]
            path.lineTo(*pos_mid)
            path.lineTo(self.pos_dst[0], self.pos_dst[1])  # 终点
            self.end_direction = [np.sign(self.pos_dst[0]-pos_mid[0]), np.sign(self.pos_dst[1]-pos_mid[1])]
        return path

	# override
    def boundingRect(self):
        return self.shape().boundingRect()

	# override
    def shape(self):
        return self.calc_path()

	# override
    def paint(self, painter, graphics_item, widget=None):
        self.setPath(self.calc_path()) # 设置路径
        path = self.path()
        if self.edge_wrap.end_item is None:
        	# 包装类中存储了线条开始和结束位置的图元
        	# 刚开始拖拽线条时，并没有结束位置的图元，所以是None
        	# 这个线条画的是拖拽路径，点线
            painter.setPen(self._pen_dragging)
            painter.drawPath(path)
        else:
        	# 这画的才是连接后的线
            painter.setPen(self._pen)
            painter.drawPath(path)

class Edge:
    def __init__(self, scene, start_item, end_item):
    	# 参数分别为场景、开始图元、结束图元
        self.scene = scene
        self.start_item = start_item
        self.end_item = end_item

		# 线条图形在此处创建
        self.gr_edge = GraphicEdge(self)
        # 此类一旦被初始化就在添加进scene
        self.scene.add_edge(self.gr_edge)

		# 开始更新
        if self.start_item is not None:
            self.update_positions()

        # edge join in terminal
        if self.end_item is not None:
            self.start_item.add_edge(self.gr_edge)
            self.end_item.add_edge(self.gr_edge)

	# 最终保存进scene
    def store(self):
        self.scene.add_edge(self.gr_edge)

	# 更新位置
    def update_positions(self):
    	# src_pos 记录的是开始图元的位置，此位置为图元的左上角
        src_pos = self.start_item.pos()
        src_group = self.start_item.group()
        if src_group:
            src_pos = src_group.mapToScene(src_pos)
        # # 想让线条从图元的中心位置开始，让他们都加上偏移
        # patch = self.start_item.width / 2
        # self.gr_edge.set_src(src_pos.x()+patch, src_pos.y()+patch)
        self.gr_edge.set_src(src_pos.x(), src_pos.y())
        # 如果结束位置图元也存在，则做同样操作
        if self.end_item is not None:
            end_pos = self.end_item.pos()
            end_group = self.end_item.group()
            if end_group:
                end_pos = end_group.mapToScene(end_pos)
            # self.gr_edge.set_dst(end_pos.x()+patch, end_pos.y()+patch)
            self.gr_edge.set_dst(end_pos.x(), end_pos.y())
        else:
            # self.gr_edge.set_dst(src_pos.x()+patch, src_pos.y()+patch)
            self.gr_edge.set_dst(src_pos.x(), src_pos.y())
        self.gr_edge.update()

    def remove_from_current_items(self):
        self.end_item = None
        self.start_item = None

	# 移除线条
    # 从场景中移除item发生奔溃以及显示残留的问题： https://blog.csdn.net/ko1234634/article/details/115217250 , https://bbs.csdn.net/topics/399169120
    def remove(self):
        self.remove_from_current_items()
        self.scene.remove_edge(self.gr_edge)
        # 释放内存, removeItem不会主动释放内存
        self.gr_edge = None

class Line(QGraphicsLineItem):
    def __init__(self, start_item, end_item, parent=None):
        super().__init__(parent)
        self.start_item = start_item
        self.end_item   = end_item
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.color = "black"

    def boundingRect(self):
        rect = QRectF(-self.width/2, -self.height/2, self.width, self.height)
        return rect

    def updatePosition(self):
        pass

import sys
from PyQt5.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import Qt, QPointF, QPoint
from PyQt5.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.scene = QGraphicsScene(self)
        # self.view = QGraphicsView(self)
        self.scene = GraphicScene(self)
        self.view = GraphicView(self.scene, self)
        # 有view就要有scene
        self.view.setScene(self.scene)
        # 设置view可以进行鼠标的拖拽选择
        self.view.setDragMode(self.view.RubberBandDrag)

        # item = GraphicItem(Power)       # 创建图元
        # item.setPos(QPointF(100,100))   # 坐标系是场景坐标系，即图元被摆放在场景的(100,100)处
        # self.scene.add_node(item)        # 将图元加到场景中

        item = GraphicItemGroup(NMOS)       # 创建图元
        item.setPos(QPointF(100,100))   # 坐标系是场景坐标系，即图元被摆放在场景的(100,100)处
        self.scene.add_node(item)        # 将图元加到场景中

        item = GraphicItemGroup(GND)       # 创建图元
        item.setPos(QPointF(200,100))   # 坐标系是场景坐标系，即图元被摆放在场景的(100,100)处
        self.scene.add_node(item)        # 将图元加到场景中

        item = GraphicItemGroup(NMOS)       # 创建图元
        item.setPos(QPointF(100,300))   # 坐标系是场景坐标系，即图元被摆放在场景的(100,100)处
        self.scene.add_node(item)        # 将图元加到场景中

        item = GraphicItemGroup(PMOS)       # 创建图元
        item.setPos(QPointF(100,400))   # 坐标系是场景坐标系，即图元被摆放在场景的(100,100)处
        self.scene.add_node(item)        # 将图元加到场景中

        # item = GraphicItem(NPN)       # 创建图元
        # item.setPos(QPointF(200,200))   # 坐标系是场景坐标系，即图元被摆放在场景的(100,100)处
        # self.scene.add_node(item)        # 将图元加到场景中

        # item = GraphicItem(PNP)       # 创建图元
        # item.setPos(QPointF(200,300))   # 坐标系是场景坐标系，即图元被摆放在场景的(100,100)处
        # self.scene.add_node(item)        # 将图元加到场景中

        item = GraphicItemGroup(Voltage)       # 创建图元
        item.setPos(QPointF(200,300))   # 坐标系是场景坐标系，即图元被摆放在场景的(100,100)处
        self.scene.add_node(item)        # 将图元加到场景中

        item = Point()       # 创建图元
        item.setPos(QPointF(400,400))   # 坐标系是场景坐标系，即图元被摆放在场景的(100,100)处
        self.scene.add_node(item)        # 将图元加到场景中

        self.setMinimumHeight(500)
        self.setMinimumWidth(500)
        self.setCentralWidget(self.view)
        self.setWindowTitle("Graphics Demo")

def demo_run():
    app = QApplication(sys.argv)
    demo = MainWindow()
    # 适配 Retina 显示屏（选写）.
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    # ----------------------------------
    demo.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    demo_run()