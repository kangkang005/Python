from copy import deepcopy
from bnf import *


class Item0:
    def __init__(self, name, rule: Rule, pos) -> None:
        self._name = name   # name 是产生式的左部
        self._rule = rule   # rule 是产生式的右部
        self._pos = pos     # pos 是点号右边的元素在列表中的索引

    def __str__(self) -> str:
        s = [self._name, ' ::= ']
        for i in range(len(self._rule)):
            if i == self._pos:
                s.append('• ')
            s.extend((self._rule[i], ' '))
        if self._pos == len(self._rule):
            s.append('•')
        return ''.join(s)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Item0):
            return False
        return __o._name == self._name and __o._rule == self._rule and __o._pos == self._pos

    # 这个方法拷贝当前对象，把点号后移一位，返回拷贝的对象
    def Move(self):
        if self._pos < len(self._rule):
            moved = deepcopy(self)
            moved._pos += 1
            return moved
        return None

    # 返回点号后面的元素；
    # 如果只返回 pos 的值，后面还需要再回过头来索引它对应的值。
    def Where(self):
        if self._pos < len(self._rule):
            return self._rule[self._pos]
        return None

    @property
    def name(self):
        return self._name

    @property
    def Index(self):
        return self._rule.Index


class LRState:
    def __init__(self) -> None:
        # 这里的 name 是 LRState 的 name，
        # 相当于教科书上的 I0、I1 等等等等
        # 和上面的 name 没有任何关系！
        self.__name = 0
        # items 是放 Item0 类的实例的
        self.__items = []

    # 下面这个是可读可写的 name 属性
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    def __iter__(self):
        return (item for item in self.__items)

    def __getitem__(self, i):
        return self.__items[i]

    def __setitem__(self, i, value):
        self.__items[i] = value

    # foo = LRState()
    # bar = len(foo)
    def __len__(self):
        return len(self.__items)

    # foo = LRState()
    # foo += Item0(bar1, bar2, 0)
    # 碰到 += 的时候 Python 就会调用 iadd 函数。
    def __iadd__(self, value):
        if value not in self.__items:
            self.__items.append(value)
        return self

    def __str__(self) -> str:
        s = [str(self.name), ':\n']
        for item in self.__items:
            s.extend(['\t', str(item), '\n'])
        return ''.join(s)

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, LRState):
            return False
        return self.__items == __o.__items


def closureLR0(items: LRState, nts: NonTerminals):
    # 这个函数不需要返回什么东西。
    # 因为它会原址向 items 参数添加内容。
    # 我承认这样的设计很别扭，但好处是可以避免复制对象的开销。
    old = 0

    while len(items) != old: # 一个项集里有多少 LR(0) 项？
        old = len(items)
        for item in items:  # 让 items 变得可以遍历是 __iter__ 的作用
            name = item.Where() # 点号右边是什么？
            if name and name[0] == '<': # 如果是非终结符（所有非终结符都用尖括号括着）
                for rule in nts[name]:  # 遍历这个非终结符对应的所有产生式右部
                    items += Item0(name, rule, 0)
                    # 这里不需要向上面的伪代码里那样检查产生式是不是已经在 items 里，
                    # 因为 __iadd__ 会检查的。嗯，这样设计似乎不太好。


def goto(items: LRState, symbol: str, nts: NonTerminals, findclosure):
    gotoset = LRState()     # 新建一个空项集
    for item in items:      # 遍历项集中所有的条目，确定点号右边是不是 symbol
        name = item.Where()
        if name == symbol:
            gotoset += item.Move() # 如果是的话，就把它单抽出来，把点号右移一位，再放到那个空项集里。

    # 遍历完之后，返回这个新项集的闭包
    if len(gotoset) != 0:
        findclosure(gotoset, nts)
        return gotoset
    return None


def GetStates(init: LRState, nts: NonTerminals, startSymbol: str, findclosure):
    # 为什么找闭包的函数是 GetStates 函数的参数……
    # 因为构造 LR(1) 自动机和项集的算法和构造 LR(0) 的几乎一模一样，
    # 只有找闭包的函数不同。
    transition = dict() # 用来表示 GOTO 函数的数据结构：字典
    statenumber = 1     # statenumber 是 LR(0) 项集的编号

    findclosure(init, nts)  # 作为参数传入 GetStates 函数的 init 里面
    # 只有一个项，形如 S' → • S。它的闭包是 LR(0) 自动机的初态，编号是 0.
    C = [init,]
    symbols = nts.GetName()  # GetName 方法返回所有非终结符的集合。嗯，封装字典的方便之处原来体现在这里了。
    symbols.extend(nts.GetTermName())  # GetTermName 方法返回所有终结符的集合。

    old = 0
    while len(C) != old:
        old = len(C)

        for i in range(old): # 如果还有新项集被添加到 C 中，就一遍一遍又一遍地找项集
            for symbol in symbols:  # 遍历符号集合
                newstate = goto(C[i], symbol, nts, findclosure) # 找 GOTO(I, X) 对应的项集
                if newstate and (newstate not in C):    # 如果是个新项集
                    newstate.name = statenumber         # 给它编号
                    # 设置“转移函数”，更新状态编号。
                    # Python 里的元组（tuple）是不可变元素，
                    # 所以可以拿来索引字典。
                    transition[(C[i].name, symbol)] = statenumber
                    statenumber += 1
                    C.append(newstate)
                elif newstate and newstate in C: # 如果所谓“newstate”已经在 C 里面了
                    index = C.index(newstate)
                    transition[(C[i].name, symbol)] = C[index].name

    # 最后设置一下哪个状态碰到了 eof 之后切到接受状态
    stateBeforeAccept = transition[(0, startSymbol)]
    transition[(stateBeforeAccept, 'eof')] = 'Accept!'
    return C, transition


def test():
    print("##### item #####")
    item = Item0('<S\'>', ['<S>',], 0)
    move_item = item.Move()
    print(item)
    print(item.Where())
    print(move_item)
    print(move_item.Where())
    print(item == move_item)

if __name__ == '__main__':
    nts = ParseBNF('simplegrammar.txt').Build()

    init = LRState()
    init += Item0('<S\'>', ['<S>',], 0)
    c, transition = GetStates(init, nts, '<S>', closureLR0)

    for state in c:
        print(state)
    for (key, value) in transition.items():
        print(key, ':', value, sep=' ')

    test()