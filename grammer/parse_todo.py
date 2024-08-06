# @grammar: TODO, DEDENT is newline, NAME is line
# todo-plus ::= todo-list EOF | EOF
# todo-list ::= todo | todo-list todo
# todo      ::= item | item INDENT todo-list DEDENT | item INDENT DEDENT | INDENT DEDENT
# item      ::= NAME

# without dedent, but not appropriate for building AST
# todo      ::= INDENT* NAME todo | EOF

# item      ::= name NEWLINE*
# todo-dict ::= item INDENT todo DEDENT todo-dict | EOF
# todo      ::= todo-list+ | todo-dict+
# todo-list ::= item

# @example:
# test1:
#     ☐ test list1 @started(19-12-11 21:16)
#     > test list1 comm
#     ✔ test list2 @critical @started(19-12-11 21:16) @done(19-12-11 21:17) @lasted(1m2s)
#     ✘ cancel @cancelled(19-12-11 21:28)
#     test2:
#         ☐ test list21 @started(19-12-11 21:16)
#         ✔ test list22 @critical @started(19-12-11 21:16) @done(19-12-11 21:17) @lasted(1m2s)
#         ✘ test list23 cancel @cancelled(19-12-11 21:28)
#     test3:
#         ☐ test list21 @started(19-12-11 21:16)
#
# test3:
#     ☐ test list31 @started(19-12-11 21:16)
#     ✔ test list32 @critical @started(19-12-16 09:24) @done(19-12-16 09:24) @lasted(41s)

# @analyse:
# NAME: test1:
# INDENT
# NAME: ☐ test list1 @started(19-12-11 21:16)
# NAME: ✘ cancel @cancelled(19-12-11 21:28)
# NAME: test2:
# INDENT
# NAME: ☐ test list21 @started(19-12-11 21:16)
# NAME: ✘ test list23 cancel @cancelled(19-12-11 21:28)
# DEDENT
# DEDENT
# NAME: test3:
# INDENT
# NAME: ☐ test list31 @started(19-12-11 21:16)
# DEDENT
# EOF

import json
import os
import sys
import re
from copy import deepcopy
from collections import OrderedDict
from pprint import *
import traceback
from pyecharts import options as opts
from pyecharts.charts import Page, Tree

# Token
NAME = 'NAME' # 等于
EOF = 'EOF'  # 结束符号
INDENT = 'INDENT'  # 缩进
DEDENT = 'DEDENT'  # 退格
NEWLINE = "NEWLINE" # 换行

##############################################
#  Lexer   词法分析器                         #
##############################################
class Token:  # 定义记号类
    def __init__(self, type, value):  # 定义构造方法
        self.type  = type  # 记号中值的类型
        self.value = value  # 记号中的值

    def __str__(self):  # 重写查看记号内容的方法
        return 'Token({type},{value})'.format(type=self.type, value=self.value)

    def __repr__(self):  # 也可以写成 __repr__=__str__
        return self.__str__()

class Lexer():       #词法分析器
    def __init__(self, text):  # 定义构造方法获取用户输入的表达式
        self.text = text  # 用户输入的表达式
        self.position = 0  # 获取表达式中每一个字符时的位置
        self.current_char = self.text[self.position]  # 设置当前字符为指定位置的字符
        self.mark_stack = []

    def mark(self):
        breakpoint = {
            "position"      :    self.position,
            "current_char"  :    self.current_char,
        }
        self.mark_stack.append(breakpoint)
        return breakpoint

    def release(self):
        breakpoint = self.mark_stack.pop(-1)
        self.position       = breakpoint["position"]
        self.current_char   = breakpoint["current_char"]
        return breakpoint

    def error(self):  # 定义提示错误的方法
        raise Exception('警告：错误的输入内容！')  # 抛出异常

    def advance(self):  # 定义获取下一个字符的方法
        self.position += 1  # 获取字符的位置自增
        if self.position >= len(self.text):  # 如果位置到达字符串的末尾
            self.current_char = None  # 设置当前字符为None值
        else:  # 否则
            self.current_char = self.text[self.position]  # 设置当前字符为指定位置的字符
        return self.current_char

    # todo
    def indent(self):
        string = ""
        flag = True
        for i in range(4):
            if self.current_char != " ":
                flag = False
                break
            string += self.current_char
            self.advance()
        if flag:
            return Token(INDENT, string)
        else:
            self.error()

    def name(self):
        string = ""
        while not self.current_char == "\n":
            string += self.current_char
            self.advance()
        return Token(NAME, string)

    def skip_newline(self):
        self.advance()

    def skip_whitespace(self):  # 定义跳过空格的方法
        while self.current_char is not None and self.current_char.isspace():  # 如果当前字符不是None值并且当前字符是空格
            self.advance()  # 获取下一个字符

    # LL(k), LL(1) is that looks next one char, LL(k) is that looks next k chars
    # peek not consume any char
    def peek(self, k = 1):
        pos = self.position + k  # 获取下一个位置
        if pos >= len(self.text):  # 如果超出文本末端
            return None  # 返回None
        else:  # 否则
            return self.text[pos]  # 返回下一位置字符

    def get_next_token(self):
        while self.current_char is not None:  # 如果当前字符不是None值
            if self.current_char == "\n":
                self.skip_newline()
                continue
            if self.current_char == " ":
                return self.indent()
            if self.current_char != "\n":
                return self.name()
            self.error()  # 如果以上都不是，则抛出异常。
        return Token(EOF, None)  # 遍历结束返回结束标识创建的记号对象

    def analyse(self):
        self.tokens = []
        while self.current_char is not None:
            token = self.get_next_token()
            self.tokens.append(token)
            print(token)
        return self.tokens

class IndentLexer(Lexer):
    def __init__(self, text):
        super(IndentLexer, self).__init__(text)
        self.indent_stack = []
        self.col = 0
        self.row = 0

    def advance(self):  # 定义获取下一个字符的方法
        self.col += 1
        self.position += 1  # 获取字符的位置自增
        if self.position >= len(self.text):  # 如果位置到达字符串的末尾
            self.current_char = None  # 设置当前字符为None值
        else:  # 否则
            self.current_char = self.text[self.position]  # 设置当前字符为指定位置的字符
        return self.current_char

    def newline(self):
        self.row += 1
        self.advance()
        self.col = 0
        return Token(NEWLINE, "")

    def name(self):
        if self.indent_stack:
            prev_indent, prev_row, prev_col = self.indent_stack[-1]
            if self.indent_stack and prev_col > self.col :
                prev_indent, prev_row, prev_col = self.indent_stack.pop(-1)
                return Token(DEDENT, "")

        string = ""
        while not self.current_char == "\n":
            string += self.current_char
            self.advance()
        return Token(NAME, string)

    def indent(self):
        string = ""
        flag = True
        for i in range(4):
            if self.current_char != " ":
                flag = False
                break
            string += self.current_char
            self.advance()
        if not flag:
            self.error()

        token = Token(INDENT, string)
        if self.indent_stack:
            prev_indent, prev_row, prev_col = self.indent_stack[-1]
            if self.col <= prev_col:
                flag = False
            else:
                self.indent_stack.append((token, self.row, self.col))
        else:
            self.indent_stack.append((token, self.row, self.col))
        if flag:
            return token
        return None

    def eof(self):
        if self.indent_stack:
            self.indent_stack.pop(-1)
            return Token(DEDENT, "")
        return Token(EOF, None)  # 遍历结束返回结束标识创建的记号对象

    # NOTE: get_next_token best to generator
    def get_next_token(self):
        while self.current_char is not None:  # 如果当前字符不是None值
            if self.current_char == "\n":
                return self.newline()
            if self.current_char == " ":
                token = self.indent()
                if token:
                    return token
                continue
            if self.current_char != "\n":
                return self.name()
            self.error()  # 如果以上都不是，则抛出异常。
        return self.eof()  # 遍历结束返回结束标识创建的记号对象

    def analyse(self):
        try:
            getattr(self, "tokens")
        except:
            self.tokens = []
        token = self.get_next_token()
        self.tokens.append(token)
        print(token)
        if token.type == EOF:
            return self.tokens
        return self.analyse()

class Parser:  #语法分析器
    def __init__(self, lexer):  # 定义构造方法获取用户输入的表达式
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token() # 语法分析器初始化
        self.remember_stack = []

    def error(self):  # 定义提示错误的方法
        raise Exception(f'''
警告：语法分析器出现错误！
Type:       {self.current_token.type}
Value:      {self.current_token.value}
Position:   {self.lexer.position-1}
Context:    {self.lexer.text[0:self.lexer.position]}''')  # 抛出异常

    def eat(self,token_type):
        # print('current_token:',self.current_token)
        if (self.current_token.type==token_type):
            self.current_token = self.lexer.get_next_token()
        else:  # 否则
            self.error()  # 抛出异常

##############################################
#  Parser   语法分析器                        #
##############################################
class AST(object):
    pass

# key name or function name
class Name(AST):  # 添加变量节点
    def __init__(self, token):
        self.token = token  # 记号
        self.name = token.value  # 变量值

class Block(AST):  # 添加变量节点
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def get_child(self):
        yield self.left
        if isinstance(self.right, list):
            for child in self.right:
                yield child
        else:
            yield self.right

class Dictionary(AST):
    def __init__(self, nodes):
        self.dictionaries = nodes

    def get_child(self):
        for child in self.dictionaries:
            yield child

class TodoParser(Parser):
    def parser(self):
        node = self.todo()  # 获取程序所有节点
        if self.current_token.type != EOF:  # 如果当前不是文件末端记号
            self.error()  # 抛出异常
        return node  # 返回程序节点

    def todo(self):
        if self.current_token.type == EOF:
            return
        while self.current_token.type == INDENT:
            self.eat(INDENT)
        self.eat(NAME)
        self.todo()

class NewTodoParser(Parser):
    def parser(self):
        # node = self.todo_plus()  # 获取程序所有节点
        # node = self.todo()  # 获取程序所有节点
        node = self.todo_dict()  # 获取程序所有节点
        if self.current_token.type != EOF:  # 如果当前不是文件末端记号
            self.error()  # 抛出异常
        return node  # 返回程序节点

    def item(self):
        node = Name(self.current_token)
        self.eat(NAME)
        self.eat(NEWLINE)
        while self.current_token.type == NEWLINE:
            self.eat(NEWLINE)
        return node

    def block(self):
        nodes = []
        self.eat(INDENT)
        while self.current_token.type == NAME:
            nodes.append(self.todo())
        self.eat(DEDENT)
        return nodes

    # #  right recursion, not easy to create AST
    # def todo_dict(self):
    #     if self.current_token.type == EOF:
    #         return
    #     node = self.todo()
    #     self.todo_dict()

    def todo_dict(self):
        nodes = []
        nodes.append(self.todo())
        while self.current_token.type != EOF:
            nodes.append(self.todo())
        # return nodes
        return Dictionary(nodes=nodes)

    def todo(self):
        left_node = self.item()
        right_node = None
        if self.current_token.type == INDENT:
            right_node = self.block()
        return Block(left=left_node, right=right_node) # list or dict

##############################################
#  NodeVisitor  AST树访问基类                 #
##############################################
class NodeVisitor(object):
    def visit(self, node):  # 节点遍历
        # 获取节点类型名称组成访问器方法名（子类Interpreter中方法的名称）
        # print(node)
        method_name = 'visit_' + type(node).__name__
        # 获取访问器对象，找不到访问器时获取“generic_visit”
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class SemanticAnalyzer(NodeVisitor):  # 添加语义分析器
    def __init__(self):
        pass

    def visit_Name(self, node):  # 添加与访问变量声明相关的访问方法
        pass

    def visit_Block(self, node):  # 添加与访问变量声明相关的访问方法
        self.visit(node.left)
        if node.right:
            for cell in node.right:
                self.visit(cell)

    def visit_Dictionary(self, node):  # 添加与访问变量声明相关的访问方法
        for dictionary in node.dictionaries:
            self.visit(dictionary)

##############################################
#  Interpreter  解释器                        #
##############################################
class Interpreter(NodeVisitor):
    def __init__(self, tree):  # 修改构造方法
        self.tree = tree  # 获取参数AST
        self.GLOBAL_MEMORY = OrderedDict()  # 创建全局存储字典

    def visit_Name(self, node):  # 访问数字类型节点的方法
        return node.name

    def visit_Block(self, node):  # 添加与访问变量声明相关的访问方法
        key = self.visit(node.left)
        value = []
        if node.right:
            for cell in node.right:
                value.append(self.visit(cell))
        if value:
            return {key:value}
        return key

    def visit_Dictionary(self, node):  # 添加与访问变量声明相关的访问方法
        result = []
        for dictionary in node.dictionaries:
            result.append(self.visit(dictionary))
        return result

    def interpret(self):  # 执行解释的方法
        tree = self.tree  # 获取AST
        if tree is None:  # 如果AST不存在
            return ''  # 返回空字符串
        return self.visit(tree)  # 否则访问AST

##############################################
#  Listener  监听器                           #
##############################################
class NodeListener(object):
    def __init__(self):
        self.stack = []

    def visitTerminal(self, node):
        if node is None:
            return
        # print(type(node).__name__)
        method_name = 'exit_' + type(node).__name__
        listen = getattr(self, method_name, "")
        return listen(node)

    def visitErrorNode(self, node):
        pass

    def enterEveryRule(self, node):
        self.stack.append(node)

    def exitEveryRule(self, node):
        element = self.stack.pop(-1)

    def enterRule(self, node):
        pass

    def exitRule(self, node):
        method_name = 'exit_' + type(node).__name__
        listen = getattr(self, method_name, "")
        return listen(node)

class TodoListener(NodeListener):  # 添加语义分析器
    def __init__(self):
        super(TodoListener, self).__init__()

    def exit_Name(self, node):
        print("Name :", node.name)

    def exit_Block(self, node):
        print("Block :", node.left, node.right)

    def exit_Dictionary(self, node):
        print("Dictionary :", node.dictionaries)

class ParserTreeWalk():
    def __init__(self):
        pass

    def walk(self, listener, tree):
        if tree is None or isinstance(tree, Name):
            listener.visitTerminal(tree)
            return
        # elif isinstance(tree, ErrorNode):
        #     listener.visitErrorNode(tree)
        #     return

        # 中序遍历
        # enter
        self.enterRule(listener, tree)
        # TODO: visitor tree children, how to unify tree children method
        # print(tree)
        for child in tree.get_child():
            self.walk(listener, child)
        # exit
        self.exitRule(listener, tree)

    def enterRule(self, listener, node):
        listener.enterEveryRule(node)
        listener.enterRule(node)

    def exitRule(self, listener, node):
        listener.exitEveryRule(node)
        listener.exitRule(node)

def main():
    if 1 :
        txt = """test1:
    ☐ test list1 @started(19-12-11 21:16)
    > test list1 comm
    ✔ test list2 @critical @started(19-12-11 21:16) @done(19-12-11 21:17) @lasted(1m2s)
    ✘ cancel @cancelled(19-12-11 21:28)
    test2:
        ☐ test list21 @started(19-12-11 21:16)
        ✔ test list22 @critical @started(19-12-11 21:16) @done(19-12-11 21:17) @lasted(1m2s)
        ✘ test list23 cancel @cancelled(19-12-11 21:28)
        test31:
            do nothing


test3:
    ☐ test list31 @started(19-12-11 21:16)
    ✔ test list32 @critical @started(19-12-16 09:24) @done(19-12-16 09:24) @lasted(41s)
    test4:
        ☐ test list21 @started(19-12-11 21:16)
"""
        print(txt)
        # lexer = Lexer(txt)
        # lexer.analyse()

        # print('\n开始语法分析...')
        # parser = TodoParser(lexer)
        # tree = parser.parser()

        lexer = IndentLexer(txt)
        # lexer.analyse()

        print('\n开始语法分析...')
        parser = NewTodoParser(lexer)
        tree = parser.parser()

        print('\n开始语义分析...')
        semantic_analyzer  = SemanticAnalyzer()
        semantic_analyzer.visit(tree)
        # print(semantic_analyzer.symbol_table)

        print('\n开始解释代码...')
        interpreter = Interpreter(tree)
        result = interpreter.interpret()
        pprint(result)

        if 1:
            walk = ParserTreeWalk()
            walk.walk(TodoListener(), tree)

if __name__ == "__main__":
    main()