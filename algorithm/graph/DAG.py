from Graph import Graph

def demo():
    g = Graph()
    for i in range(6):
        g.addVertex(i)

    g.addEdge(0,1,5)
    # g.addEdge(0,5,2)
    g.addEdge(1,2,4)
    g.addEdge(2,3,9)
    g.addEdge(3,4,7)
    g.addEdge(3,5,3)
    # g.addEdge(4,0,1)
    g.addEdge(5,4,8)
    # g.addEdge(5,2,1)

    g.print_graph()
    return g

def is_DAG(g):
    # 是否是DAG（有向无环图）
    isDAG = True
    # 标记矩阵,0为当前结点未访问,1为访问过,-1表示当前结点后边的结点都被访问过。
    color = {vertex.getId(): 0 for vertex in g}

    def dfs(vertex):
        nonlocal isDAG
        # 标记成已经访问过的状态为1
        color[vertex.getId()] = 1
        for other_vertex in vertex.getConnections():
            # 被访问过
            if color[other_vertex.getId()] == 1:
                # 有环
                isDAG = False
                break
            elif color[other_vertex.getId()] == -1:
                # 当前结点后边的结点都被访问过，直接跳至下一个结点
                continue
            else:
                dfs(other_vertex)
        # 遍历过所有相连的结点后，把本节点标记为-1
        color[vertex.getId()] = -1

    for vertex in g:
        dfs(vertex)
    return isDAG

print(is_DAG(demo()))

# 拓扑排序应用：
# 1:任务调度系统中的拓扑排序应用
# 2:课程安排与选课系统中的应用
#   大学课程的学习是有先后顺序的，C 语言是基础，数据结构依赖于 C 语言，其它课程也有类似依赖关系。
# 3:软件工程中的依赖关系管理
#   假设 VS 中有三个项目 A,B，C,
#   3.1. A->B->C 不存在循环引用
#   3.2. A->B->C->A 存在循环引用, 报错
def topology_sort_bfs(g):
    # 创建入度字典
    in_degrees = {vertex: 0 for vertex in g}
    # 获取每个节点的入度
    for vertex in g:
        for other_vertex in vertex.getConnections():
            in_degrees[other_vertex] += 1

    # 使用列表作为队列并将入度为0的添加到队列中
    queue = [vertex for vertex in g if in_degrees[vertex] == 0]
    res = []
    while queue:
        # 从队列首部取出元素
        vertex = queue.pop(0)
        # 将取出的元素存入结果中
        res.append(vertex.getId())
        # 移除与取出元素相关的指向，即将所有与取出元素相关的元素的入度减少1
        for other_vertex in vertex.getConnections():
            in_degrees[other_vertex] -= 1
            # 若被移除指向的元素入度为0，则添加到队列中
            if in_degrees[other_vertex] == 0:
                queue.append(other_vertex)
    return res

print(topology_sort_bfs(demo()))