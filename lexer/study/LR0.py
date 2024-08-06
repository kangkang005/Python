from pprint import *
# @web: https://www.jianshu.com/p/cd31a159d86e
# 变量申明
ACTION = []
GOTO = []
grams = [] # 用于存放文法字符串 ["S->cA", "S->ccB", "A->cA", "A->a", "B->ccB", "B->b"]
grams = ["S->cA", "S->ccB", "A->cA", "A->a", "B->ccB", "B->b"]
grams = ["S->A", "S->B", "A->aAb", "A->c", "B->aBb", "B->d"]
grams = ["S->S+T", "S->T", "T->(S)", "T->a"]
dot_grams = []
VN = []
VN2Int = {}  # 非终结符映射
VT2Int = {}  # 终结符映射
VT = []
Vs = []
items = []
dnf_array = []

location = 0  # 输入位置
status_stack = []  # 状态栈
symbol_stack = []  # 符号栈
now_state = ''  # 栈顶状态
input_ch = ''  # 栈顶字符
input_str = ''  # 输入串
now_step = 0  # 当前步骤

# print(grams)
#------------------预处理---------------#
grams = ["S->AB",
         "S->bC",
         "A->$",
         "A->b",
         "B->$",
         "B->aD",
         "C->AD",
         "C->b",
         "D->aS",
         "D->c"]

def first_set(non_terminal):
    result = set()
    visit = set()
    non_terminal_set = {gram.split("->")[0] for gram in grams}
    for gram in grams:
        left, right = gram.split("->")
        if left == non_terminal:
            if gram in visit:
                continue
            else:
                visit.add(gram)
            if right[0] in non_terminal_set:
                null_num = 0
                # 若 X∈VN；Y1，Y2，…，Yi∈VN，且有产生式 X→Y1 Y2 … Yn；当 Y1 Y2 … Yn-1 都能推导出 ε 时，则 FIRST (Y1)、FIRST (Y2)、…、FIRST (Yn-1) 的所有非空元素和 FIRST (Yn) 包含在 FIRST (X) 中。
                for char in right:
                    first = first_set(char)
                    result |= first - {"$"}
                    if "$" not in first:
                        break
                    else:
                        null_num += 1
                # 如果右式推导都含有空串，加入空串
                # 若 X∈VN，且有产生式 X→a…，a∈VT， 则 a∈FIRST (X) X→ε, 则 ε∈FIRST (X)。　（简单讲，若是非终结符 X，能推导出以终结符 a 开头的串，那么这个终结符 a 属于 FIRST（X），若 X 能够推导出空符号串 ε，那么空符号串 ε 也属于 X 的 FIRST 集）
                if len(right) == null_num:
                    result |= {"$"}
            else:
                result.add(right[0])
    return result

def follow_set(non_terminal, visit_non_terminal=set()):
    result = set("$")
    visit = set()
    # grams = ["S->Bc", "S->d", "B->aS", "B->Sb"]
    for gram in grams:
        left, right = gram.split("->")
        if non_terminal in right:
            if gram in visit:
                continue
            else:
                visit.add(gram)
            follow_index = right.find(non_terminal)
            if not follow_index == len(right)-1:
                follow = right[follow_index+1]
                # follow may be non-terminal or terminal
                for item in first_set(follow):
                    result.add(item)
            else:
                # B->aS , S follow set include B follow set
                # 防止non_terminal在深度搜索中重复出现
                # 例如：grams = ["S->AB", "S->bC", "A->$", "A->b", "B->$", "B->aD", "C->AD", "C->b", "D->aS", "D->c"]
                # follow_set("S")
                visit_non_terminal.add(non_terminal)
                if left not in visit_non_terminal:
                    result |= follow_set(left, visit_non_terminal=visit_non_terminal)
    return result

# 划分终结符和非终结符
def get_v():
    vn_num = 0
    vt_num = 0
    for s in grams:
        x,y = s.split("->")
        # print(x,y)
        if(x not in VN):
            VN.append(x)
            VN2Int.update({x: vn_num})
            vn_num = vn_num + 1
        for v in y:
            if(v.isupper()):
                if(v not in VN):
                    VN.append(v)
                    VN2Int.update({v: vn_num})
                    vn_num = vn_num + 1
            else:
                if(v not in VT):
                    VT.append(v)
                    VT2Int.update({v: vt_num})
                    vt_num = vt_num + 1

    for vn in VN:
        Vs.append(vn)
    for vt in VT:
        Vs.append(vt)

    VT.append("#")
    VT2Int.update({"#": vt_num})
    print("得到非终结符集合 VN："+ str(VN))
    print("得到终结符集合 VT：" + str(VT))
    print("所有的符号集合 Vs：" + str(Vs))

def dot_gram():
    # 为所有产生式加点
    dot_grams.append("S'->.S")
    dot_grams.append("S'->S.")

    for gram in grams:
        ind = gram.find("->")
        for i in range(len(gram)-ind-1):
            tmp = gram[:ind+2+i] + "." + gram[ind+2+i:]
            # print(tmp)
            dot_grams.append(tmp)

#------------构造DNF代码---------------------#
def get_VN_gram(v):
    # 返回非终结符产生的A->.aBb形式
    res = []
    for gram in dot_grams:
        ind = gram.find("->")
        # NOTE:会引入S'->S式子
        if(gram[0]==v and gram[ind+2]=="."):
            res.append(gram)
    return res

def get_VN_gram(v):
    # 返回非终结符产生的A->.aBb形式
    res = []
    for gram in dot_grams:
        ind = gram.find("->")
        left, right = gram.split("->")
        if left == v and right[0] == ".":
            res.append(gram)
    return res

# print(get_VN_gram("A"))

def get_CLOSURE(grammar):
    # 生成闭包
    CLOSURE = []
    for it in grammar:
        # 先加入A→α・Bβ的产生式
        if(it not in CLOSURE):
            CLOSURE.append(it)
        x, y = it.split(".")
        # 跳过・后为空串的产生式，如A→α・产生式
        if(y == ""):
            continue
        # 对于・后为非终结符的产生式，如A→α・Bβ的产生式，继续查找B有关的产生式并加入到闭包当中
        v = y[0]
        if(v in VN):    # 非终结符
            res = get_VN_gram(v)     # 返回非终结符A产生的A->.aBb形式
            for re in res:
                if(re not in CLOSURE):
                    CLOSURE.append(re)
    return CLOSURE

# BFS
def get_CLOSURE(grammar):
    CLOSURE = []
    while grammar:
        it = grammar.pop(0)
        if(it not in CLOSURE):
            CLOSURE.append(it)
        x, y = it.split(".")
        # 跳过・后为空串的产生式，如A→α・产生式
        if(y == ""):
            continue
        # 紧跟着.后面的字符
        v = y[0]
        if(v in VN):    # 非终结符
            res = get_VN_gram(v)     # 返回非终结符A产生的A->.aBb形式
            for re in res:
                if(re not in CLOSURE):
                    CLOSURE.append(re)
                    grammar.append(re)
    return CLOSURE

def is_inItems(new_item):
    #判断item是否已经存在, 存在返回位置，不存在返回-1
    if(new_item == None):
        return -1

    new_set = set(new_item)
    num=0
    for item in items:
        old_set = set(item)
        if(old_set == new_set):
            return num
        num = num + 1

    return -1

def go(item, v):
    #生成并返回下一个item
    go_one_char_item = []
    for it in item:
        x, y = it.split(".")
        if(y!="" and y[0] == v):
            # .向前走一个字符
            new_it = x + y[0] + "." + y[1:]
            go_one_char_item.append(new_it)
    if not go_one_char_item:
        return
    go_one_char_item = get_CLOSURE(go_one_char_item)
    #print(tmp)
    #print("go(item, "+v + ") = " + str(go_one_char_item))
    # print(go_one_char_item)
    return go_one_char_item

def get_items():
    #构建item的集合

    # 初始化,生成I0
    item = []
    init_s = "S'->.S"
    item.append(init_s)
    dot_gram()
    # print(dot_grams)

    # print(item)
    # for it in item:
    #     v = it[it.find(".")+1]
    #     if(v in VN):
    #         res = get_VN_gram(v)
    #         for re in res:
    #             if(re not in item):
    #                 item.append(re)

    # 第一次closure只会找到.后为非终结符的产生式，还需要第二次closure才会找到.后为非终结符和终结符的产生式
    # item = get_CLOSURE(get_CLOSURE(item))
    # new version: use BFS can avoid closure again
    item = get_CLOSURE(item)
    print("I0 is :" + str(item))
    items.append(item)

    num=0
    for item in items:
        for v in Vs:
            # print("item is %s," % str(item) + "v is %s" % v)
            new_item = go(item, v)

            # 判断状态不为空，且不存在于原状态中
            if (new_item != None):
                if (is_inItems(new_item) == -1):
                    # print("添加了%s" % str(new_item))
                    items.append(new_item)

    # print_items()
    pprint(items)

# BFS
def get_items():
    #构建item的集合

    # 初始化,生成I0
    item = []
    init_s = "S'->.S"
    item.append(init_s)
    dot_gram()

    # 加入第一个项集
    item = get_CLOSURE(item)
    print("I0 is :" + str(item))
    items.append(item)
    queue = [item]
    while queue:
        item = queue.pop(0)
        for v in Vs:
            new_item = go(item, v)
            if new_item is not None:
                if (is_inItems(new_item) == -1):
                    queue.append(new_item)
                    items.append(new_item)
    # pprint(items)

# get_v()
# get_items()

#---------------构造LR(0)表代码--------------#
def init_lr_table():
    action_len = len(VT)
    goto_len = len(VN)
    for h in range(len(items)):
        ACTION.append([])
        GOTO.append([])
        for w1 in range(len(VT)+1):
            ACTION[h].append("  ")
        for w2 in range(len(VN)):
            GOTO[h].append("  ")
    # print(ACTION) # row is items, col is VT+1
    # print(GOTO)   # row is items, col is VN

def lr_is_legal():
    # 判别lr是否合法
    has_protocol = 0 #是否存在规约项目
    has_shift = 0 #是否存在移进项目

    for item in items:
        for it in item:
            x, y = it.split(".")
            if(y ==""):
                if(has_protocol != 0 or has_shift != 0):
                    return False
                has_protocol = 1
            else:
                if(y[0] in VT):
                    has_shift = 1
    return True


# 找到该项在文法中的索引, S'->S不在初始文法中
def find_gram(it):
    x, y = it.split(".")
    mgram = x+y
    try:
        ind = grams.index(mgram)
        return ind
    except ValueError:
        return -1

dot_gram()
# print(dot_grams[1])
# print(find_gram(dot_grams[1]))

def get_lr_table():
    #构建lr分析表
    init_lr_table()
    lr_is_legal()
    i=0
    j=0
    for item in items:
        for it in item:
            x, y = it.split(".")
            if(y==""): #判断是否写入ACTION
                if (it == "S'->S."):
                    ACTION[i][len(VT)-1] = "acc"
                ind = find_gram(it)
                if(ind != -1):
                    # 规约
                    for k in range(len(ACTION[i])):
                        ACTION[i][k]="r"+str(ind+1)

            else:
                next_item = go(item, y[0])
                # print("go(%s, %s)-->%s" % (str(item), y[0], str(next_item)))
                ind = is_inItems(next_item)
                if(ind != -1): #判断是否写入GOTO
                    if y[0] in VT:
                        j = VT2Int[y[0]]
                        ACTION[i][j] = "s" + str(ind)
                    if y[0] in VN:
                        j = VN2Int[y[0]]
                        GOTO[i][j] = ind
        i = i + 1
    print_lr_table()

#-----------------规约------------------#
def is_end():
    if input_str[location:len(input_str)] == '#':
        if symbol_stack[-1] == 'S' and symbol_stack[-2] == '#':
            return True
        else:
            return False
    else:
        return False

    return True

# 输出
def output():
    global now_step, status_stack, symbol_stack, input_str, now_state
    print('%d\t\t' % now_step, end='')
    now_step += 1
    print('%-20s' % status_stack, end='')
    print('%-50s' % symbol_stack, end='')
    print('%-30s' % input_str[location:len(input_str)], end='')

# 统计产生式右部的个数
def count_right_num(grammar_i):
    return len(grammar_i) - 3


def stipulations():
    # 根据LR(0)表进行规约

    # location初始为0
    global location
    print('----分析过程----')
    print("index\t\t", end='')
    print('%-20s' % 'Status', end='')
    print('%-50s' % 'Symbol', end='')
    print('%-30s' % 'Input', end='')
    print('Action')
    for i in range(len(dot_grams)):
        print('---', end='')
    print()

    symbol_stack.append('#')
    status_stack.append(0)
    while not is_end():
        now_state = status_stack[-1]
        input_ch = input_str[location]
        if(input_ch not in (Vs + VT)):
            print("错误字符")
            return -1
        output()
        # 通过输入字符和当前状态找到下一个状态
        find = ACTION[now_state][VT2Int[input_ch]]

        if find[0] == 's': # 进入action
            symbol_stack.append(input_ch)
            status_stack.append(int(find[1]))
            # 跳转到下一个字符
            location += 1
            print('action[%s][%s]=s%s, 移入%s' % (now_state, input_ch, find[1], input_ch))

        elif find[0] == 'r': # 进入goto
            num = int(find[1])
            g = grams[num - 1] # 找出该式子在初始文法中的位置
            right_num = count_right_num(g)
            #print("\n%s"%g)
            for i in range(right_num):
                status_stack.pop()
                symbol_stack.pop()
            # 移入左式
            symbol_stack.append(g[0])
            now_state = status_stack[-1]
            symbol_ch = symbol_stack[-1]
            find = GOTO[now_state][VN2Int.get(symbol_ch, -1)]
            if find == -1:
                print('分析失败')
                return -1
            status_stack.append(find)
            print('归约%s' % g)
        else:
            return -1

    print("\n is done")
    return 0

#----------------print代码--------------#

def print_grams():

    print("----产生式集合----")
    num = 1
    for gram in grams:
        print("(%d)%s"%(num, str(gram)))
        num = num + 1

def print_items():

    print("----状态集合----")
    num=0
    for it in items:
        print("(%d)%s"%(num, str(it)))
        num = num + 1

def print_lr_table():
    # 表头
    print('----LR分析表----')
    print(f"{' '*8}|{' '*4}", end='')
    print(('%4s' % '') * (len(VT) - 3), end='')
    print('Action', end='')
    print(('%4s' % '') * (len(VT) - 3), end='')
    print(f"{' '*5}|{' '*8}", end='')
    print(('%3s' % '') * (len(VN) - 2), end='')
    print('GOTO', end='')
    print(('%3s' % '') * (len(VN) - 2), end='')
    print(f"{' '*5}|")
    print(f"{' '*16}", end='')
    for i in VT:
        print('%4s' % i, end='')
    print(f"{' '*4}|{' '*8}", end='')
    k = 0
    for i in VN:
        print('%3s%1s' % (i, " "), end='')
    print('\t|')
    for i in range(len(dot_grams)):
        print('---', end='')
    print()
    # 表体
    for i in range(len(items)):
        print('%5d\t|\t' % i, end='')
        for j in range(len(VT)):
            print('%4s' % ACTION[i][j], end='')
        print('\t|\t', end='')
        for j in range(len(VN)):
            if not GOTO[i][j] == -1:
                print('%4s' % GOTO[i][j], end='')
            else:
                print('\t', end='')
        print('\t|')
    for i in range(len(dot_grams)):
        print('---', end='')
    print()

if __name__ == '__main__':
    if(len(grams)==0):
        with open("1.txt", "r") as f:
            for line in f:
                line = line.replace('\n', "")
                grams.append(line)
            f.close()

    get_v()     # 分割终结符和非终结符
    print_grams()    # 输出文法产生式
    get_items()     # 生成状态集合
    print_items()   # 输出状态集合
    get_lr_table()  # 生成lr分析表
    # input_str = "abaaabaaab#"  # 待分析字符串
    # input_str = "a+(a)#"  # 待分析字符串
    # input_str = "(a)+a#"  # 待分析字符串
    input_str = "a+a#"  # 待分析字符串
    stat = stipulations()   #规约
    if(stat == 0):
        print("\n %s 符合文法规则" % input_str)
    else:
        print("\n %s 不符合文法规则" % input_str)

    # print(follow_set("T"))
    # print(first_set("S"))
    # print(follow_set("A"))