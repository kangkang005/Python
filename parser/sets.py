from bnf import *
from leftrec import *


def makechanging():
    length = None

    # 嵌套的函数——检查字典 d 中集合的长度是否发生变化。
    def changing(d: dict) -> bool:
        nonlocal length
        # 第一次调用创建记录字典 d 集合长度的字典变量 length
        if not length:
            length = dict()
            for k in d.keys():
                length[k] = len(d[k])
            return True

        # 再次调用检查 d 中集合的长度是否发生变化。
        isChanging = False
        for k in d.keys():
            isChanging |= (length[k] != len(d[k]))
            length[k] = len(d[k])
        return isChanging

    return changing


def FirstSet(nts: NonTerminals, ts: list) -> dict:
    # ts：终结符列表。终结符用 str 表示。
    # nts：非终结符及其对应的若干产生式体。
    # 这个字典的键为 str，表示具体的非终结符。
    # 值为列表的列表，存放对应的产生式体。
    # 比如键“C”对应的值可以是
    # [['"c"', '<C>'], ['"d"']]
    # 为了方便区分，我们把所有非终结符都用尖括号（“<>”）括起来。
    # 用双引号括起来的和没有被括起来的都是终结符。
    # 空串（ε）用 "" 表示。
    first = dict()
    # 非终结符
    for (name, rules) in nts:
        first[name] = set()
    # 终结符
    for terminal in ts:
        first[terminal] = {terminal}

    changing = makechanging()

    while changing(first):
        # 这两层 for 循环的作用是遍历所有产生式
        for (name, rules) in nts:
            for rule in rules:
                if rule != ['""',]:
                    # rhs: Right Hand Side，指右值
                    rhs = deepcopy(first[rule[0]])
                    rhs.discard('""')
                    # 先拷贝产生式箭头右侧第一个符号的 FIRST 集
                    # 之后遍历产生式右侧的所有符号
                    for i in range(0, len(rule) - 1):
                        # 如果某个非终结符可以推出空串就继续循环
                        if '""' not in first[rule[i]]:
                            # 对于非终结符 X->Y1 Y2 ... Yn, 如果 Y1 ... Yi 都能推导出ε，但是 Yi+1 不能推导出ε，则 {First(Y1)-ε} ⋃ ... ⋃ {First(Yi)-ε} ⋃ First(Yi+1) ⊆ First(X)
                            break
                        # {First(Yi)-ε}, first集的非空集合
                        rhs |= first[rule[i + 1]]
                        rhs.discard('""')
                    # for 循环执行后，额外执行 else 语句，若循环中断，则不执行额外的 else 语句
                    else:
                        # 如果上面的 for 循环正常终止就会跳到这里
                        if '""' in first[rule[-1]]:
                            # 对于非终结符 X->Y1 Y2 ... Yn, 如果Y1 ... Yn 都能推导出ε，则 X->ε，即 ε ∈ First(X)
                            rhs.add('""')
                else:
                    rhs = {'""'}
                # 最后，把本轮循环求出来的终结符集合和
                # 产生式头对应的 FIRST 集合合并到一起
                first[name] |= rhs

    return first


def FollowSet(nts: NonTerminals, first: dict, startsymbol: str) -> dict:
    follow = dict()
    for (name, rules) in nts:
        follow[name] = set()
    # 1. 开始符号（比如上面的 “S”）的 FOLLOW 集里面总有一个 EOF 符号。先把它放进去。
    if startsymbol:
        follow[startsymbol].add('eof')
        # 开始符号的 FOLLOW 集里总是有 eof。先把它放进去。
        # 其实龙书上用的是“$”。
        # 不过我觉得直接用“eof”会比用“$”看起来舒服一点。

    changing = makechanging()

    # 和上面一样，反复求 FOLLOW 集直到所有 FOLLOW 集都不再变化为止
    while changing(follow):
        for (name, rules) in nts:
            for rule in rules:
                trailer = deepcopy(follow[name])
                # 先初始化 trailer：相当于把 FOLLOW(A) 先存下来
                for i in range(len(rule) - 1, -1, -1):
                    # 从右至左遍历产生式体中的符号
                    # “<>”括着的都是非终结符
                    if rule[i][0] == '<': # rule[i] is a non-terminal
                        # 3. 如果产生式形如  A→αB 或者虽形如 A→αBβ 但 FIRST(β) 中包含 ε，就把 FOLLOW(A) 中的符号全放到 FOLLOW(B) 中。
                        follow[rule[i]] |= trailer
                        # 如果最里层 for 循环的首轮迭代就调用这一行的话，
                        # 它能起到上面第三点的作用

                        # 以下的 if-else 语句对应上面的第二点
                        # 到了下一轮迭代就可以改 FOLLOW 集了
                        if '""' in first[rule[i]]:
                            # 2. 如果产生式形如 A->αBβ，那就把 FIRST (β) 里除 ε 之外的所有符号都放到 FOLLOW (B) 里。
                            trailer |= first[rule[i]]
                            trailer.discard('""')
                        else:
                            trailer = deepcopy(first[rule[i]])
                    else:  # 否则就只修改 trailer，不修改其他非终结符的 FOLLOW 集
                        trailer = deepcopy(first[rule[i]])

    return follow


if __name__ == '__main__':
    nts = ParseBNF('grammar.txt').Build()
    nts = EliminateLeftRecursion(nts)
    ts = ['"+"', '"-"', '"*"', '"/"', '"%"', '"^"', 'num', '"("', '")"', '""', 'eof']
    first = FirstSet(nts, ts)
    follow = FollowSet(nts, first, '<expr>')

    for (name, firstset) in first.items():
        print('%s: ' % name, firstset, sep=' ')
    print()
    for (name, followset) in follow.items():
        print('%s: ' % name, followset, sep=' ')