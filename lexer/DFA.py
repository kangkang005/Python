class DFANode(object):
    def __init__(self, name=None, isFinal=0):
        super(DFANode, self).__init__()
        # name：表示该节点的名称，作为节点的唯一标识
        self.name = name
        # isFinal：表示该节点是否是终态, 1 is final, 0 is not ending
        self.isFinal = isFinal
        # edge：表示该节点与其他节点的转换关系
        self.edge = {}

    # addEdge (alpha,target)：用于为该节点增加与其他节点的转换关系
    def addEdge(self, alpha, target):
        if alpha not in self.edge:
            nextNodes = set()
            nextNodes.add(target)
            self.edge[alpha] = nextNodes
        else:
            self.edge[alpha].add(target)

class DFA(object):
    def __init__(self, terminators):
        super(DFA, self).__init__()
        # status 属性：DFANode 的集合，包含该 DFA 的所有节点和节点之间转换关系
        self.status = {}
        # terminators 属性：表示该 DFA 对应的终结符集合
        self.terminators = terminators