from NFA import NFA, NFANode
from DFA import DFA, DFANode

digit = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
symbol = [',', ';', '[', ']', '(', ')', '{', '}', '+', '-', '*', '/', '%', '^', '&', '=', '~', '<', '>']
keyword = ['int', 'double', 'char', 'float', 'break', 'continue', 'do', 'while', 'if', 'else', 'for', 'void', 'return', 'scanf', 'print', 'function']


class LexAnalyze(object):
    def __init__(self):
        super(LexAnalyze, self).__init__()
        # productions：表示产生式列表
        self.productions = []       # 产生式列表
        #  alphabets：表示字符集合
        self.alphabets = {}
        # keywords：表示关键词集合
        self.keywords = {}
        # NFA：表示正规文法对应的 NFA
        self.NFA = None
        # DFA：表示 NFA 确定化后的 DFA
        self.DFA = None

        self.alphabets['alphabet'] = set(alphabet)
        self.alphabets['digit'] = set(digit)
        self.alphabets['symbol'] = set(symbol)
        for word in keyword:
            self.keywords[word] = 'keyword'

    # readLexGrammar (filename)：读取正规文法，得到产生式列表、关键词集合和字符集合
    def readLexGrammar(self, filename):
        cur_left = None
        cur_right = []
        line_num = 0
        for line in open(filename, 'r'):
            # skip comment
            if line[0] == "#":
                continue
            line = line.split('\n')[0]
            index = line.find(':')
            cur_left = line[0:index]
            cur_right = line[index + 1:len(line)]
            line_num += 1

            production = {}
            production['left'] = cur_left
            index = cur_right.find(' ')

            # 右边有非终结符
            if index != -1:
                # before whitespace
                production['input'] = cur_right[0:index]
                # after whitespace
                production['right'] = cur_right[index + 1:len(cur_right)]

            # 右边没有非终结符
            else:
                # cur_right is terminal
                production['input'] = cur_right
                production['right'] = None
            self.productions.append(production)

    # createNFA ()：由产生式列表构造 NFA
    # 将正则表达式转换为 NFA 的算法称为 Thompson 构造法。
    # 算法的基本思路就是：通过递归地将一个正则表达式划分成构成它的子表达式，在得到每个子表达式对应的 NFA 之后，根据子表达式之间的运算关系和一系列规则构造表达式自身对应的 NFA。
    # 简单来说就是不管多复杂的 NFA 都可以通过多个简单的 NFA（像我们前面看到的那么简单）组合而成。
    def createNFA(self):
        all_status = {}

        # isFinal：表示该节点是否是终态, 1 is final, 0 is not ending
        def getNFANode(name, isFinal):
            if name in all_status:
                node = all_status[name]
            else:
                node = NFANode(name=name, isFinal=isFinal)
            return node

        start_node = getNFANode('start', 0)
        end_node = getNFANode('end', 1)
        all_status['start'] = start_node
        all_status['end'] = end_node
        for prod in self.productions:
            # print(prod)
            now = prod['left']
            alpha = prod['input']
            next = prod['right']
            now_node = getNFANode(now, 0)

            # 右边有非终结符，指向对应节点
            if next is not None:
                target_node = getNFANode(next, 0)

            # 输入字符不是由 'digit' 'nonzero_digit' 'alphabet' 表示的终结符，即alpha自身是一个终结符
            if alpha not in self.alphabets.keys():
                if next is None:
                    # alpha is terminal, alpha -> end
                    now_node.addEdge(alpha, 'end')
                else:
                    if next in self.alphabets.keys():
                        # next is terminal
                        for val in self.alphabets[next]:
                            now_node.addEdge(alpha, val)
                    else:
                        # next is non-terminal
                        now_node.addEdge(alpha, next)

            # 输入字符是由 'digit' 'nozero_digit' 'alphabet' 表示的终结符
            else:
                for val in self.alphabets[alpha]:
                    if next is None:
                        # alpha is terminal, val -> end
                        # for example: {'left': 'integer', 'input': 'digit', 'right': None}
                        #   0 -> end
                        #   ...
                        #   9-> end
                        now_node.addEdge(val, 'end')
                        # print(prod)
                        # print(now_node.edge)
                        # {'left': 'scientific_tail', 'input': 'digit', 'right': None}
                        # {'5': {'end'}, '6': {'end'}, '9': {'end'}, '1': {'end'}, '7': {'end'}, '3': {'end'}, '2': {'end'}, '8': {'end'}, '0': {'end'}, '4': {'end'}}
                    else:
                        # alpha is non-terminal
                        if next in self.alphabets.keys():
                            # next is terminal
                            for tval in self.tool_set[next]:
                                now_node.addEdge(alpha, tval)
                        else:
                            # next is non-terminal
                            now_node.addEdge(alpha, next)
                            now_node.addEdge(val, next)

            # 更新NFA中的节点信息
            all_status[now] = now_node
            if next is not None:
                all_status[next] = target_node

        # NFA的终结符集合，待思考
        terminators = set()
        for i in range(ord(' '), ord('~') + 1):
            terminators.add(chr(i))
        self.NFA = NFA(terminators)
        self.NFA.status = all_status
        # {'start': <NFA.NFANode object at 0x00000259CF591DF0>, 'end': <NFA.NFANode object at 0x00000259CF5919A0> ...
        # print(all_status)

    # createDFA ()：将 NFA 确定化为 DFA : 子集构造法
    # 子集构造法的基本思想是让构造得到的 DFA 的每个状态对应 NFA 的一个状态集合。DFA 在读入a1a2...an之后到达的状态应该对应于相应的 NFA 从开始状态出发，沿着以a1a2...an为边的路径能达到的状态的集合。
    # 使用 NFA 来匹配字符串需要两个关键操作：
    #   closure
    #   move
    # ε–closure(s)：从NFA状态s开始，只通过ε转换能到达的NFA状态集合
    # ε–closure(T)：从T中某个状态s开始，只通过ε转换能到达的NFA状态集合
    # move(T, a)：从T中某个状态s出发，通过一个标号为a的转换能到达的NFA状态集合
    def createDFA(self):
        all_status = {}

        def getDFANode(name, isFinal):
            if name in all_status:
                return all_status[name]
            else:
                node = DFANode(name, isFinal)
            return node

        # $ 表示空串 ε
        for node_name in self.NFA.status['start'].edge['$']:
            start_node = getDFANode('start', 0)
            dfa_node = getDFANode(node_name, 0)
            # for example: start:$ limiter
            #   $ -> limiter
            start_node.addEdge('$', node_name)
            all_status['start'] = start_node
            all_status[node_name] = dfa_node

            # 记录DFA节点是否已经访问过
            is_visit = set()
            queue = list()

            # 最初的NFA节点集合，即DFA节点
            nfa_node_set = set()
            nfa_node_set.add(node_name)
            queue.append((nfa_node_set, node_name))
            # print(queue)
            # [({'operator'}, 'operator')]

            # closure 操作
            # 我们利用一个栈来实现 closure 操作
            #   把传入集合里的所有节点压入栈中
            #   然后对这个栈的所有节点进行判断是否有可以直接跳转的节点
            #   如果有的话直接压入栈中
            #   直到栈为空则结束操作
            # 将T 的所有状态压入 stack 中;

            # 描述：
            # 将ε-closure(T) 初始化为T;
            # while(stack 非空)
            # {
            #   将栈顶元素t 弹出栈;
            #   for (每个满足下面条件的u : 从t 出发有一个标号为ε 的转换到达状态u)
            #     if(u 不在ε-closure(T)中){
            #       将u 加入到ε-closure（T） 中;
            #       将u 压入 栈中;
            #     }
            # }
            # BFS
            while queue:
                node_name = queue.pop(0)
                now_node_set = node_name[0]
                now_node_name = node_name[1]
                # print 'to =', top_node_name, ', df =', dfa_node_name
                now_dfa_node = getDFANode(now_node_name, 0)

                # move(I,alpha)  寻找后续状态
                for alpha in self.NFA.terminators:

                    # next节点的NFA节点集合
                    target_set = set()
                    for nfa_node_name in now_node_set:
                        nfa_node = self.NFA.status[nfa_node_name]

                        # 有出边
                        # find output state which alpha point
                        if alpha in nfa_node.edge.keys():
                            for name in nfa_node.edge[alpha]:
                                target_set.add(name)

                    # 如果target_set为空，则直接返回
                    if not target_set:
                        continue
                    next_node_name = ''
                    isFinal = 0
                    # 对target_set排序
                    tmp_list = list(target_set)
                    target_list = sorted(tmp_list)
                    for tar in target_list:
                        # next_node_name is DFA state
                        next_node_name = '%s$%s' % (next_node_name, tar)
                        isFinal += int(self.NFA.status[tar].isFinal)
                        # print(next_node_name)
                        #   $end
                        #   $end$index_tail

                    # 如果集合中有一个NFA的终态，该节点就是DFA的终态
                    if isFinal > 0:
                        isFinal = 1
                    next_dfa_node = getDFANode(next_node_name, isFinal)
                    now_dfa_node.addEdge(alpha, next_node_name)
                    all_status[now_node_name] = now_dfa_node
                    all_status[next_node_name] = next_dfa_node

                    # 该状态已经访问过，则继续
                    if next_node_name in is_visit:
                        continue

                    # 该状态未访问过，则放入队列中
                    else:
                        is_visit.add(next_node_name)
                        queue.append((target_set, next_node_name))

        # DFA的终结符集合，待思考
        terminators = set()
        for i in range(ord(' '), ord('~') + 1):
            terminators.add(chr(i))
        self.DFA = DFA(terminators)
        self.DFA.status = all_status

    # runOnDFA (line,pos)：在源程序的字符流中提取一个单词或报告错误信息
    def runOnDFA(self, line, pos):
        if line[pos] in self.alphabets['alphabet'] or line[pos] == '_':
            final_pos = pos
            final_str = ''
            while final_pos < len(line) and line[final_pos] not in self.alphabets['symbol'] and line[final_pos] != ' ':
                final_str += line[final_pos]
                final_pos += 1

            cur_pos = 0
            token = ''
            now_node = self.DFA.status['identifier']
            while cur_pos < len(final_str) and final_str[cur_pos] in now_node.edge.keys():
                token += final_str[cur_pos]
                now_node = self.DFA.status[list(now_node.edge[final_str[cur_pos]])[0]]
                cur_pos += 1

            if cur_pos >= len(final_str) and now_node.isFinal > 0:

                if token in self.keywords.keys():
                    token_type = self.keywords[token]
                else:
                    token_type = 'identifier'
                return final_pos - 1, token_type, token, 'OK'

            else:
                return final_pos - 1, None, '', '标识符不合法'

        elif line[pos] in self.alphabets['digit']:

            # 判断是否为复数
            final_pos = pos
            final_str = ''
            while final_pos < len(line) and (line[final_pos] not in self.alphabets['symbol'] or line[final_pos] == '+'
                                             or line[final_pos] == '-') and line[final_pos] != ' ':
                final_str += line[final_pos]
                final_pos += 1

            cur_pos = 0
            token = ''
            now_node = self.DFA.status['complex']
            while cur_pos < len(final_str) and final_str[cur_pos] in now_node.edge.keys():
                token += final_str[cur_pos]
                now_node = self.DFA.status[list(now_node.edge[final_str[cur_pos]])[0]]
                cur_pos += 1

            if cur_pos >= len(final_str) and now_node.isFinal > 0:
                token_type = 'number'
                return final_pos - 1, token_type, token, 'OK'

            # 判断是否为科学计数形式常量
            final_pos = pos
            final_str = ''
            while final_pos < len(line) and (line[final_pos] not in self.alphabets['symbol'] or line[final_pos] == '+'
                                             or line[final_pos] == '-') and line[final_pos] != ' ':
                final_str += line[final_pos]
                final_pos += 1

            cur_pos = 0
            token = ''
            now_node = self.DFA.status['scientific']
            while cur_pos < len(final_str) and final_str[cur_pos] in now_node.edge.keys():
                token += final_str[cur_pos]
                now_node = self.DFA.status[list(now_node.edge[final_str[cur_pos]])[0]]
                cur_pos += 1

            if cur_pos >= len(final_str) and now_node.isFinal > 0:
                token_type = 'number'
                return final_pos - 1, token_type, token, 'OK'

            # 判断是否为整型常量
            final_pos = pos
            final_str = ''
            while final_pos < len(line) and line[final_pos] not in self.alphabets['symbol'] and line[final_pos] != ' ':
                final_str += line[final_pos]
                final_pos += 1

            cur_pos = 0
            token = ''
            now_node = self.DFA.status['integer']
            while cur_pos < len(final_str) and final_str[cur_pos] in now_node.edge.keys():
                token += final_str[cur_pos]
                now_node = self.DFA.status[list(now_node.edge[final_str[cur_pos]])[0]]
                cur_pos += 1

            if cur_pos >= len(final_str) and now_node.isFinal > 0:
                token_type = 'number'
                return final_pos - 1, token_type, token, 'OK'

            return final_pos - 1, None, '', '标识符或常量不合法'

        else:
            cur_pos = pos
            token = ''
            token_type = 'limiter'
            now_node = self.DFA.status['limiter']

            # 逐个向后读取字符，并进行状态转移
            while cur_pos < len(line) and line[cur_pos] in now_node.edge.keys():
                token += line[cur_pos]
                now_node = self.DFA.status[list(now_node.edge[line[cur_pos]])[0]]
                cur_pos += 1

            # 如果到达终态，则获得一个单词
            if now_node.isFinal > 0:
                return cur_pos - 1, token_type, token, 'OK'

            cur_pos = pos
            token = ''
            token_type = 'operator'
            now_node = self.DFA.status['operator']

            # 逐个向后读取字符，并进行状态转移
            while cur_pos < len(line) and line[cur_pos] in now_node.edge.keys():
                token += line[cur_pos]
                now_node = self.DFA.status[list(now_node.edge[line[cur_pos]])[0]]
                cur_pos += 1

            # 如果到达终态，则获得一个单词
            if now_node.isFinal > 0:
                return cur_pos - 1, token_type, token, 'OK'

            cur_pos = pos
            while cur_pos < len(line) and line[cur_pos] not in self.alphabets['symbol'] \
                    and line[cur_pos] not in self.alphabets['digit'] and line[cur_pos] not in self.alphabets['alphabet'] \
                    and line[cur_pos] != '_' and line[cur_pos] != ' ':
                cur_pos += 1
            return cur_pos - 1, None, '', '未知错误'

        # for dfa_name in self.DFA.status['start'].edge['$']:
        #     cur_pos = pos
        #     token = ''
        #     token_type = dfa_name
        #     now_node = self.DFA.status[dfa_name]
        #
        #     # 逐个向后读取字符，并进行状态转移
        #     while cur_pos < len(line) and line[cur_pos] in now_node.edge.keys():
        #         token += line[cur_pos]
        #         now_node = self.DFA.status[list(now_node.edge[line[cur_pos]])[0]]
        #         cur_pos += 1
        #
        #     # 如果到达终态，则获得一个单词
        #     if now_node.isFinal > 0:
        #
        #         # 判断是否是关键字
        #         if token in self.keywords.keys():
        #             token_type = self.keywords[token]
        #         return cur_pos - 1, token_type, token
        # return pos, None, ''

    # analyze (filename)：对整个源程序进行词法分析
    def analyze(self, filename):
        line_num = 0
        lex_error = False
        token_table = []
        for line in open(filename, 'r'):
            pos = 0
            line_num += 1
            line = line.split('\n')[0]
            while pos < len(line):
                    # and not lex_error:

                # 跳过tab，回车，换行，空格
                while pos < len(line) and line[pos] in ['\t', '\n', ' ', '\r']:
                    pos += 1
                if pos < len(line):
                    pos, token_type, token, message = self.runOnDFA(line, pos)
                    if token_type is None:
                        print('Lexical error at line %s, column %s : %s' % (str(line_num), str(pos), message))
                        lex_error = True
                        # break
                    else:
                        token_table.append((line_num, token_type, token))
                        print('(%d , %s , %s)' % (line_num, token_type, token))
                    pos += 1

        # 如果未出错，那么写入token表文件
        if not lex_error:
            output = open('token_table.data', 'w+')
            for line_num, token_type, token in token_table:
                # type_of_token = token
                # if token_type == 'identifier' or token_type == 'number':
                #     type_of_token = token_type
                output.write('%d %s %s\n' % (line_num, token_type, token))
            output.close()
            return True
        return False


if __name__ == '__main__':

    lex_ana = LexAnalyze()
    lex_ana.readLexGrammar('LexGrammar.txt')
    lex_ana.createNFA()
    lex_ana.createDFA()
    lex_ana.analyze('source.cc')