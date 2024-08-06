class NFANode(object):
    def __init__(self, name=None, isFinal=0):
        super(NFANode, self).__init__()
        # name：表示该节点的名称，作为节点的唯一标识
        self.name = name
        # isFinal：表示该节点是否是终态
        self.isFinal = isFinal
        # edge：表示该节点与其他节点的转换关系
        self.edge = {}

    #  state.addEdge(input, next_state)
    #  addEdge (alpha,target)：用于为该节点增加与其他节点的转换关系
    def addEdge(self, alpha, target):
        if alpha not in self.edge:
            nextNodes = set()
            nextNodes.add(target)
            self.edge[alpha] = nextNodes
        else:
            self.edge[alpha].add(target)

class NFA(object):
    def __init__(self, terminators=None):
        super(NFA, self).__init__()
        # terminators 属性：表示该 NFA 对应的终结符集合
        self.terminators = terminators
        # status 属性：NFANode 的集合，包含该 NFA 的所有节点和节点之间转换关系
        self.status = {}