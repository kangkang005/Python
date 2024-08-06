from graphviz import Digraph

class Node(object):
    """节点类"""
    def __init__(self, elem):
        self.elem = elem
        self.lchild = None
        self.rchild = None


class Tree(object):
    """树类"""
    def __init__(self):
        self.root = None

    def add(self, elem):
        """为树添加节点"""
        node = Node(elem)
        if self.root is None:
            self.root = node
            return
        queue = [self.root]
        '''队列来存储节点'''
        while queue:
            cur_node = queue.pop(0)
            '''层次遍历，找到插入节点的位置'''
            if cur_node.lchild is None:
                cur_node.lchild = node
                return
            else:
                queue.append(cur_node.lchild)
            if cur_node.rchild is None:
                cur_node.rchild = node
                return
            else:
                queue.append(cur_node.rchild)

    # BFS
    # @web: https://blog.csdn.net/Master_chenyi/article/details/110671522
    def print_graph(self):
        if self.root is None:
            return
        dot = Digraph(comment="Binary Tree")
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            # dot.node(name = str(node.elem), label = str(node.elem))
            if node.lchild is not None:
                dot.node(name = str(node.lchild.elem), label = str(node.lchild.elem))
                dot.edge(str(node.elem), str(node.lchild.elem))
                queue.append(node.lchild)
            else:
                #生成空节点invisl，让生成的二叉树可以分清左右子树
                dot.node(name = str(node.elem)+'invisl', label = str(node.elem)+'invisl', style = 'invis')
                dot.edge(str(node.elem), str(node.elem)+'invisl', style = 'invis')

            #生成空节点invism，让生成的二叉树可以分清左右子树
            dot.node(name = str(node.elem)+'invism', label = str(node.elem)+'invism', style = 'invis')
            dot.edge(str(node.elem), str(node.elem)+'invism', style = 'invis')

            if node.rchild is not None:
                dot.node(name = str(node.rchild.elem), label = str(node.rchild.elem))
                dot.edge(str(node.elem), str(node.rchild.elem))
                queue.append(node.rchild)
            else:
                #生成空节点invisr，让生成的二叉树可以分清左右子树
                dot.node(name = str(node.elem)+'invisr', label = str(node.elem)+'invisr', style = 'invis')
                dot.edge(str(node.elem), str(node.elem)+'invisr', style = 'invis')
        dot.view()
        dot.render('binary_tree.gv', view=True)

    '''广度遍历'''
    def breadth_travel(self):
        if self.root is None:
            return
        queue = [self.root]
        while queue:
            cur_node = queue.pop(0)
            print(cur_node.elem,end=' ')
            if cur_node.lchild is not None:
                queue.append(cur_node.lchild)
            if cur_node.rchild is not None:
                queue.append(cur_node.rchild)

    # def traverse(node):
    #     <<pre-order actions>>
    #     left_val = traverse(node.left)
    #     <<in-order actions>>
    #     right_val = traverse(node.right)
    #     <<post-order actions>>
    '''先序遍历'''
    def preorder(self,node):
        if node is None:
            return
        print(node.elem,end=' ')
        self.preorder(node.lchild)
        self.preorder(node.rchild)

    '''中序遍历'''
    def inorder(self,node):
        if node is None:
             return
        self.inorder(node.lchild)
        print(node.elem,end=' ')
        self.inorder(node.rchild)

    '''后序遍历'''
    def postorder(self, node):
        if node is None:
            return
        self.postorder(node.lchild)
        self.postorder(node.rchild)
        print(node.elem,end=' ')

tree = Tree()
for i in range(10):
    tree.add(i)
print("层次遍历：")
tree.breadth_travel()
print()
print("先序遍历：")
tree.preorder(tree.root)
print()
print("中序遍历：")
tree.inorder(tree.root)
print()
print("后序遍历：")
tree.postorder(tree.root)

# 渲染二叉树
tree.print_graph()