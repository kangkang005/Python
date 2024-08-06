from pprint import pprint
# 利用⼦集构造法的实现任意 NFA 到 DFA 的转换。
# @web: https://blog.csdn.net/younger77/article/details/121709347
K = []  # NFA状态集
E = []  # NFA输入符号集
F = []  # NFA弧
S = []  # FNA初态集
Z = []  # NFA终态集
K_DFA = []  # DFA状态集
fx = []  # 状态转换函数
K += ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
E += ["a", "b"]
S += ["0"]
Z += ["10"]
F += [
    # $ is ε
    # state -> input_char -> next_state
    ["0" , "$", "1"],
    ["0" , "$", "7"],
    ["1" , "$", "2"],
    ["1" , "$", "4"],
    ["2" , "a", "3"],
    ["4" , "b", "5"],
    ["3" , "$", "6"],
    ["5" , "$", "6"],
    ["6" , "$", "1"],
    ["6" , "$", "7"],
    ["7" , "a", "8"],
    ["8" , "b", "9"],
    ["9" , "b", "10"],
]


# 输入NFA
def input_NFA():
    # a = input('请输入NFA状态集(以空格区分,以换行结束): ')
    # K.extend(a.split(' '))
    K = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    # a = input('请输入NFA输入符号集(以空格区分,以换行结束): ')
    # E.extend(a.split(' '))
    E = ["a", "b"]
    # a = input('请输入NFA初态集(以空格区分,以换行结束): ')
    # S.extend(a.split(' '))
    S = ["0"]
    # a = input('输入NFA终态集(以空格区分,以换行结束): ')
    # Z.extend(a.split(' '))
    Z = ["10"]
    # print('请输入NFA弧的条数: ')
    # n = int(input())
    # print('请输入这些弧(分别输入状态1,输入符号,状态2,以空格区分换行结束,ε表示为$)')
    # for i in range(n):
    #     a = input()
    #     t = a.split(' ')
    #     F.append(t)
    F = [
        ["0" , "$", "1"],
        ["0" , "$", "7"],
        ["1" , "$", "2"],
        ["1" , "$", "4"],
        ["2" , "a", "3"],
        ["4" , "b", "5"],
        ["3" , "$", "6"],
        ["5" , "$", "6"],
        ["6" , "$", "1"],
        ["6" , "$", "7"],
        ["7" , "a", "8"],
        ["8" , "b", "9"],
        ["9" , "b", "10"],
    ]

# ε-closure函数, NOTE:我感觉不对，只找出第一层的空串指向的状态，还需要继续搜索
def closure(I):
    for i in I:
        for f in F:
            if f[0] == i and f[1] == "$":
                if f[2] not in I:
                    I.append(f[2])
    # print(I)
    return sorted(I)  # 从小到大排序（按字典）

# BFS
# ε-closure函数, I∈ ε-closure(I)
def closure(I):
    result = []
    queue = []
    queue += I
    result += I # I∈ ε-closure(I)
    while queue:
        state = queue.pop(0)
        for production in F:
            if production[0] == state and production[1] == "$":
                queue.append(production[2])
                if production[2] not in result:
                    result.append(production[2]) # 加入空串指向的下一个状态
    result = sorted(result)
    return result

# DFS, 图论, 在图中找出该集合连续边为空串的所有集合
# ε-closure函数, I∈ ε-closure(I)
def closure(I):
    result = []
    result += I # I∈ ε-closure(I)
    def dfs(state):
        for production in F:
            if production[0] == state and production[1] == "$":
                if production[2] not in result:
                    result.append(production[2]) # 加入空串指向的下一个状态
                dfs(production[2])
    for state in I:
        dfs(state)
    result = sorted(result)
    return result

# move(I, a)函数, move 操作就是遍历当前的状态节点集合，如果符合的 edge 的条件的话就加入到下一个状态集合中，不需要BFS或者DFS
def move(I, a):
    new_I = []
    for i in I:
        for f in F:
            if f[0] == i and f[1] == a:
                if f[2] not in new_I:
                    new_I.append(f[2])
    return sorted(new_I)  # 从小到大排序（按字典）

# 判断新生成的子集是否存在,存在返回位置，不存在返回-1
def is_inDFA(new_k):
    new_set = set(new_k)
    index = 0
    for k in K_DFA:
        old_set = set(k)
        if old_set == new_set:
            return index
        index = index + 1
    return -1

# 添加到转换函数中
def myAppend(k, e, new_k):
    t = []
    t.append(k)
    t.append(e)
    t.append(new_k)
    fx.append(t)

# NFA转DFA
def NFA2DFA():
    J = closure(S)  # NFA的初态
    K_DFA.append(J)
    for k in K_DFA:
        for e in E:
            new_k = closure(move(k, e))
            if new_k is not None:   # 不存在于当前子集中，则加入
                if is_inDFA(new_k) == -1:
                    K_DFA.append(new_k)
                    myAppend(is_inDFA(k), e, is_inDFA(new_k))
                else:   # 存在于当前子集中，则不加入
                    myAppend(is_inDFA(k), e, is_inDFA(new_k))

# BFS
def wzk_NFA2DFA():
    # 如果找到子集，返回索引号即为DFA的状态编号
    def in_Dstates(new_states, Dstates):
        state_no = 0
        for states in Dstates:
            if set(states) == set(new_states):
                return state_no
            state_no += 1
        return -1

    J = closure(S)  # NFA的初态
    queue = []
    queue.append(J)
    Dstates = []    # 记录所有的DFA状态集合, 集合的索引即为状态编号
    Dstates.append(J)
    Dtran = {}      # 转换表
    while queue:
        states = queue.pop(0) # 当前的states
        for e in E: # NFA输入符号集
            next_states = closure(move(states, e))
            if next_states is None: # 如果为空，跳过
                continue
            if in_Dstates(next_states, Dstates) == -1:    # 不存在于当前子集中，则加入
                queue.append(next_states)
                Dstates.append(next_states)
            # 构造嵌套字典, 直接赋值就会报错
            if in_Dstates(states, Dstates) not in Dtran:
                Dtran[in_Dstates(states, Dstates)] = {}
            Dtran[in_Dstates(states, Dstates)][e] = in_Dstates(next_states, Dstates)
    pprint(Dstates)
    pprint(Dtran)
    return (Dstates, Dtran)

'''
//基于等价类的思想
split(S)
    foreach(character c)
        if(c can split s)
            // c can split S:
            // there exist q0, q1 that belong to S,
            // where q0->c->S', q1->c->S'' and S'!=S''
            split s into T1, ..., Tk

hopcroft()
    split all nodes into N, A
    // A is accept group, N is not accept group
    while(set is still changes)
        split(s)
'''
# @web: https://blog.csdn.net/weixin_50094312/article/details/127581508
def mini_DFA(Dstates, Dtran):
    # 根据是否为终结状态, 划分为 2 个组:
    def split_to_accept_and_not_accept_group(Dstates):
        groups = []
        accept_group = []
        not_accept_group = []
        accept = 0
        for NFA_states in Dstates:
            for NFA_state in NFA_states:
                if NFA_state in Z: # NFA终态集
                    accept = 1
            if accept:
                # 1.1 构造接受状态集合
                accept_group.append(NFA_states)
                accept = 0
            else:
                # 1.2 构造非接受状态集合
                not_accept_group.append(NFA_states)
        # 1.3 构造状态集合列表
        groups.append(accept_group)
        groups.append(not_accept_group)
        return groups

    # 获得dfa在dfa列表中的编号, 不在列表组返回-1
    def in_Dstates(new_states, Dstates):
        state_no = 0
        for states in Dstates:
            if set(states) == set(new_states):
                return state_no
            state_no += 1
        return -1

    # 判断组内的 dfa 是否可以区分
    def can_split(group, groups):
        group_tran = {}
        for e in E:
            group_tran[e] = set()
            for DFA_state in group:
                next_states = _move(DFA_state, e, Dstates)
                # 获得该dfa集合在最小化组中的编号
                mini_next_state_no = get_group_no(next_states, groups)
                group_tran[e].add(mini_next_state_no)
        # pprint(group_tran)
        for e in E:
            # 如果有其他组, 则该组经过e后指向多个组, 即指向不明确 ,说明该组可区分
            if len(group_tran[e]) != 1:
                return True
        return False

    # 转移到下一个DFA
    def _move(Dstate, edge, Dstates):
        state_no = in_Dstates(Dstate, Dstates)
        next_state_no = Dtran[state_no][edge]
        # 获得指向下一个的dfa集合
        next_Dstates = Dstates[next_state_no]
        return next_Dstates

    # 获得dfa在最小化组中的编号, 不在最小化组返回-1
    def get_group_no(states, groups):
        group_no = 0
        for group in groups:
            if in_Dstates(states, group) != -1:
                return group_no
            group_no += 1
        return -1

    # 判断最小化DFA是否已经结束
    def is_mini_DFA(groups):
        for group in groups:
            if len(group) != 1 and can_split(group, groups):
                return False
        return True

    # 判断两个 dfa 是否可以合并, 如果两个dfa经过一个字符都指向同个dfa，则认为两个dfa是等价的
    def can_combine(state1, state2):
        for e in E:
            next_state1 = Dtran[in_Dstates(state1, Dstates)][e]
            next_state2 = Dtran[in_Dstates(state2, Dstates)][e]
            if next_state1 != next_state2:
                # 两个dfa经过e都指向不同的dfa，这个两个dfa不等价
                return False
        return True

    # 组内切分
    # 将dfa组分成若干个子组，然后将子组加入到新的dfa组状态集合列表中
    def split_group(group, new_groups):
        subgroups = []
        for DFA_state in group:
            if not subgroups:
                # 先加入第一个DFA集合到子组
                subgroups.append(DFA_state)
            else:
                for state in subgroups:
                    # 如果dfa可以和子组中的dfa合并
                    if can_combine(state, DFA_state):
                        # 将dfa加入到子组中
                        subgroups.append(DFA_state)
                        break
                    else:
                        # 将dfa加入到新的子组中
                        new_groups.append([DFA_state])
        # 将子组列表中的子组加入到新的dfa组状态集合列表中
        new_groups.append(subgroups)
        return new_groups

    # 根据是否为终结状态, 划分为 2 个组:
    groups = split_to_accept_and_not_accept_group(Dstates)
    # pprint(groups)
    # 2. 判断是否满足最小化条件
    while not is_mini_DFA(groups):
        new_groups = []             # 2.1 构造新的状态集合列表
        for group in groups:        # 2.2 遍历状态集合列表
            if len(group) == 1:     # 2.2.1 如果集合中只有一个元素，直接加入新的状态集合列表
                new_groups.append(group)
            else:                   # 2.2.2 如果集合中含有多个元素，进一步切分
                split_group(group, new_groups)
        groups = new_groups
        # print(groups)
    pprint(groups)

    def create_DFA_tran(groups):
        new_Dtran = {}
        for e in E:
            for group in groups:
                # 只需要取DFA组内中第一个DFA集合，因为组内的DFA集合都指向其他同个组，不需要遍历DFA组
                one_DFA_state = group[0]
                state_no = in_Dstates(one_DFA_state, Dstates)
                next_state_no = Dtran[state_no][e]
                next_DFA_state = Dstates[next_state_no]

                group_no = get_group_no(one_DFA_state, groups)
                next_group_no = get_group_no(next_DFA_state, groups)
                # 构造嵌套字典, 避免报错keyerror
                if group_no not in new_Dtran:
                    new_Dtran[group_no] = {}
                new_Dtran[group_no][e] = next_group_no
        return new_Dtran
    new_Dtran = create_DFA_tran(groups)
    pprint(new_Dtran)

'''
    def partition(Dtran, group, first_no, next_no, input):
        goto_first = Dtran[first_no][input]
        goto_next = Dtran[next_no][input]

    need_split = True
    while need_split:
        need_split = True
'''


# 打印DFA
def print_DFA():
    print("NFA子集构造法构造出的子集：")
    for k in K_DFA:
        print(K_DFA.index(k), end=": ")
        print(k)
    # 矩阵形式
    print("DFA矩阵表示：")
    print("\\", end="\t")
    for e in E:
        print(e, end="\t")
    print()
    for i in range(len(K_DFA)):
        print(i, end="\t")
        for e in E:
            for f in fx:
                if i == f[0] and e == f[1]:
                    print(f[2], end="\t")
                    break
                if fx.index(f) == len(fx) - 1:
                    print("", end="\t")
        for j in K_DFA[i]:
            if j in Z:
                print("(终态)", end=" ")
                break
        print()

if __name__ == '__main__':
    input_NFA()
    NFA2DFA()
    print_DFA()
    (Dstates, Dtran) = wzk_NFA2DFA()
    mini_DFA(Dstates, Dtran)