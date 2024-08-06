# https://blog.csdn.net/kkkjfg/article/details/129713215
import copy
'''
                pin location
       a  b  c  d  e  f  g  h  i  j  k
top = [0, B, D, E, B, F, G, 0, D, 0, 0]
bot = [A, C, E, C, E, A, F, H, 0, H, G]

routing[A] = {a,b,c,d,e,f}
routing[B] = {b,c,d,e}
routing[C] = {b,c,d}
...
'''

# Horizontal Constraint Graphs
def HCG(top, bottom):
    merge = [{_top, _bottom} for _top, _bottom in zip(top, bottom)]
    distance = {}
    for idx, horizontals in enumerate(merge):
        for horizontal in horizontals:
            distance.setdefault(horizontal, []).append(idx)
    # 0 代表轨道未连接任何的线
    distance.pop(0, None)
    # print(distance)

    # S(col)为水平线经过列col或者有引脚在col上的网络的集合
    S_col = {}
    for idx in range(len(merge)):
        for horizontal in distance:
            if distance[horizontal][0] <= idx <= distance[horizontal][-1]:
                S_col.setdefault(idx, set()).add(horizontal)
    # print(S_col)

    # 类似冒泡排序
    def find_HCG():
        result = {}
        copy_S_col = copy.deepcopy(S_col)
        for outside in S_col:
            copy_S_col.pop(outside)
            for inside in copy_S_col:
                intersection = copy_S_col[inside] & S_col[outside]
                if intersection != copy_S_col[inside] and intersection != S_col[outside]:
                    result[inside] = copy_S_col[inside]
                else:
                    if copy_S_col[inside] > S_col[outside]:
                        result.pop(outside, None)
                        # S(col)包含网络数的最大值
                        result[inside] = copy_S_col[inside]
                    else:
                        result.pop(inside, None)
        return result
    result = find_HCG()
    # print(result)
    return result

# Vertical Constraint Graphs
def VCG(top, bottom):
    result = {}
    for _top, _bottom in zip(top, bottom):
        result.setdefault(_top, set()).add(_bottom)
    result.pop(0, None)
    for horizontal in result:
        if 0 in result[horizontal]:
            result[horizontal].remove(0)
    # print(result)

    # 为了简洁，绘制垂直约束图的时候要注意删去冗余边，若存在三条这样的边 (G–>F),(F–>A),(G–>A), 我们会把 G 指向 A 的那条边删掉。
    # 有向无环图的 Transitive Reduction 算法
    # https://blog.csdn.net/wyzidu/article/details/117789524

    # 计算每个节点的非直接依赖节点
    # print(result)
    # @方法一：暴力dfs
    def find_indirect_dependent_node():
        indirect_node_result = {}
        all_paths = []
        path = []
        def dfs(cur, path=None):
            if not path:
                path = []
            for elem in result[cur]:
                path.append(elem)
                if len(path) > 2:
                    for indirect_node in path[0:-2]:
                        indirect_node_result.setdefault(indirect_node, set()).add(elem)
                if elem in result:
                    dfs(elem, path)
                else:
                    all_paths.append(copy.deepcopy(path))
                    # print(path)
                path.pop(-1)
        for key in result:
            path.append(key)
            dfs(key, path)
            path.pop(-1)
        # print(indirect_node_result)
        return indirect_node_result

    def find_intersection(indirect_dict, direct_dict):
        intersection_dict = {}
        for key in indirect_dict:
            if key in direct_dict:
                intersection_set = direct_dict[key] & indirect_dict[key]
                if intersection_set:
                    intersection_dict[key] = intersection_set
        return intersection_dict
    direct_dependent_node   = result
    indirect_dependent_node = find_indirect_dependent_node()
    remove_redundant_node   = find_intersection(indirect_dependent_node, direct_dependent_node)
    # print(remove_redundant_node)

    # remove redundant node from result dictionary
    for horizontal in result:
        if horizontal in remove_redundant_node:
            result[horizontal] -= remove_redundant_node[horizontal]

    # @方法二：拓扑排序
    # 此方法不行：存在多个拓扑序列，无法找出拓扑排序
    '''
    1.获取拓扑排序序列
    2.针对拓扑排序中的每两个节点之间的边, i 从 [1, n-1], j 从 [i - 1, 0]，判断原 DAG 中是否存在
    3.若存在，则判断标记位是否为 False, 若是则将当前边添加到新 DAG 中，并将标记位置为 True
    4.判断标记位是否为 True, 若是则标记以 j 为结束节点的相关节点为 True, 直至结束
    def remove_redundant_edge_by_topology_sort():
        def get_topology_sort():
            in_degree = {}
            for key in result:
                if not key in in_degree:
                    in_degree[key] = 0
                for val in result[key]:
                    if not val in in_degree:
                        in_degree[val] = 1
                    else:
                        in_degree[val] += 1
            # print(in_degree)
            # TODO
    # remove_redundant_edge_by_topology_sort()
    '''
    return result

if __name__ == "__main__":
    top    = [0, "B", "D", "E", "B", "F", "G", 0, "D", 0, 0]
    bottom = ["A", "C", "E", "C", "E", "A", "F", "H", 0, "H", "G"]

    top    = ["B", 0, "B", "C", "D", "B", "C"]
    bottom = ["A", "C", "A", "B", 0, "B", "C"]

    top    = [0, "B", "D", "B", "A", "C", "E"]
    bottom = ["D", "C", "E", "F", 0, "A", "F"]

    top    = [0, "A", "D", "E", "A", "F", "G", 0, "D", "I", "J", "J"]
    bottom = ["B", "C", "E", "C", "E", "B", "F", "H", "I", "H", "G", "I"]
    hcg = HCG(top, bottom)
    print(hcg)
    vcg = VCG(top, bottom)
    print(vcg)