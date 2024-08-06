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

# @reference_web: https://zhuanlan.zhihu.com/p/390039110

# Token
INTEGER = 'INTEGER'  # 整数类型
REAL = 'REAL'  # 实数类型
INTEGER_CONST = 'INTEGER_CONST'  # 整数（因子）
REAL_CONST = 'REAL_CONST'  # 实数（因子）
PLUS = 'PLUS'  # 加
MINUS = 'MINUS'  # 减
MUL = 'MUL'  # 乘
INTEGER_DIV = 'INTEGER_DIV'  # 整数除法
FLOAT_DIV = 'FLOAT_DIV'  # 浮点数除法
LPAREN = 'LPAREN'  # 左括号
RPAREN = 'RPAREN'  # 右括号
LBRACE = 'LBRACE'  # 左花括号
RBRACE = 'RBRACE'  # 右花括号
ID = 'ID'  # 变量名称
ASSIGN = 'ASSIGN'  # 赋值符号
BEGIN = 'BEGIN'  # 开始标记
END = 'END'  # 结束标记
SEMI = 'SEMI'  # 分号
DOT = 'DOT'  # 点（程序结束符）
PROGRAM = 'PROGRAM'  # 程序
VAR = 'VAR'  # 变量声明标记
COLON = 'COLON'  # 冒号
COMMA = 'COMMA'  # 逗号
EOF = 'EOF'  # 结束符号
PROCEDURE = 'PROCEDURE'  # 过程
STRING = 'STRING' # 字符串
EQUAL = 'EQUAL' # 等于
COMMENT = 'COMMENT' # 注释

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

RESERVED_KEYWORDS = {  # 保留字
    'PROGRAM': Token(PROGRAM, 'PROGRAM'),
    'PROCEDURE': Token(PROCEDURE, 'PROCEDURE'),  # 保留字
    'VAR': Token(VAR, 'VAR'),
    'DIV': Token(INTEGER_DIV, 'DIV'),
    'INTEGER': Token(INTEGER, 'INTEGER'),
    'REAL': Token(REAL, 'REAL'),
    'BEGIN': Token(BEGIN, 'BEGIN'),
    'END': Token(END, 'END'),
}

class Lexer():       #词法分析器
    def __init__(self, text):  # 定义构造方法获取用户输入的表达式
        self.text = text  # 用户输入的表达式
        self.position = 0  # 获取表达式中每一个字符时的位置
        self.current_char = self.text[self.position]  # 设置当前字符为指定位置的字符
        self.mark_stack = [] # 暂时保存当前字符和位置

    def mark(self):     # 记录当前字符和位置
        breakpoint = {
            "position"      :    self.position,
            "current_char"  :    self.current_char,
        }
        self.mark_stack.append(breakpoint)
        return breakpoint

    def release(self):  # 回退到之前所保存的字符和位置
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

    def skip_whitespace(self):  # 定义跳过空格的方法
        while self.current_char is not None and self.current_char.isspace():  # 如果当前字符不是None值并且当前字符是空格
            self.advance()  # 获取下一个字符

    # comment ::= "/*" <any char> "*/"
    def skip_comment(self):  # 添加跳过注释内容到的方法
        comment = ""
        while not (self.current_char == '*' and self.peek() == "/"):  # 如果当前字符不是注释结束符号
            comment += self.current_char
            self.advance()  # 提取下一个字符
        # print(comment)
        # consume end of comment */
        self.advance()  # 提取下一个字符*（跳过注释结束符号）
        self.advance()  # 提取下一个字符/（跳过注释结束符号）
        return Token(COMMENT, comment)

    # LL(k), LL(1) is that looks next one char, LL(k) is that looks next k chars
    # peek not consume any char
    def peek(self, k = 1): # 往前看第k个字符, 但是不消耗字符
        pos = self.position + k  # 获取下一个位置
        if pos >= len(self.text):  # 如果超出文本末端
            return None  # 返回None
        else:  # 否则
            return self.text[pos]  # 返回下一位置字符

    def _id(self):  # 获取保留字或赋值名称记号的方法
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == "_"):  # 如果当前字符是字母数字
            result += self.current_char  # 连接字符
            self.advance()  # 提取下一个字符
        # port identifier
        if self.current_char == "[": # 将带有序号的引脚也视为id, 例如A[1]
            while self.current_char is not None and not self.current_char == "]":
                result += self.current_char
                self.advance()  # 提取下一个字符
            result += self.current_char
            self.advance()  # 提取下一个字符]（port结束符号）
        token = RESERVED_KEYWORDS.get(result.upper(), Token('ID', result))  # 如果是保留字返回保留字记号，默认返回ID记号
        #upper():使关键词支持不区分大小写
        return token

    def number(self):  # 获取数字
        result = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):  # 如果当前字符不是None值并且当前字符是数字
            result += self.current_char  # 连接数字
            self.advance()  # 获取下一个字符
        if ('.' in result):
            return Token(REAL_CONST,float(result))  # 返回浮点数
        else:
            return Token(INTEGER_CONST,int(result))  # 返回整数

    # @web: https://www.cnblogs.com/yubo-guan/p/18021690
    # <floating-point-number> ::= <digit-sequence> ['.' <digit-sequence>] [<exponent>]
    # <exponent>              ::= 'e' ['+' | '-'] <digit-sequence>
    # <digit-sequence>        ::= <digit> | <digit-sequence> <digit>
    # <digit>                 ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
    def number(self):
        result = ""
        result += self.digit_sequence()
        if self.current_char is not None and self.current_char == ".": # 解析小数部分
            result += self.current_char
            self.advance()
            result += self.digit_sequence()
        if self.current_char is not None and self.current_char.lower() == "e": # 解析指数部分
            result += self.current_char
            self.advance()
            if self.current_char is not None and self.current_char in ["-", "+"]:
                result += self.current_char
                self.advance()
            result += self.digit_sequence()
        if ('e' in result):
            return Token(REAL_CONST,float(result))  # 返回浮点数
        elif ('.' in result):
            return Token(REAL_CONST,float(result))  # 返回浮点数
        else:
            return Token(INTEGER_CONST,int(result))  # 返回整数

    def digit_sequence(self): # 解析数字序列
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char  # 连接数字
            self.advance()  # 获取下一个字符
        return result

    # string ::= "'" string_item* "'" | """ string_item* """
    def long_string(self):
        result = ""
        while self.current_char is not None and not self.current_char == "\"":
            result += self.current_char
            self.advance()
        self.advance()
        return Token(STRING, result)

    def short_string(self):
        result = ""
        while self.current_char is not None and not self.current_char == "\'":
            result += self.current_char
            self.advance()
        self.advance()
        return Token(STRING, result)

    # 双重while循环进行词法扫描
    def get_next_token(self):   # 获取下一个词
        while self.current_char is not None:  # 如果当前字符不是None值
            if self.current_char.isspace():  # 如果当前字符是空格
                self.skip_whitespace()  # 跳过所有空格
                continue
            if self.current_char == '/' and self.peek() == '*':  # 注释
                # consume start of comment /*
                self.advance()  # 跳到下一字符
                self.advance()  # 跳到下一字符
                result = self.skip_comment()    # 跳过所有注释
                # continue
                return result
            if self.current_char.isdigit():  # 如果当前字符是整数
                result = self.number()  # 获取完整的数字创建记号对象并返回
                # print(result)
                return result
            if self.current_char == '+':  # 如果当前字符是加号
                self.advance()  # 跳到下一字符
                return Token(PLUS, '+')  # 创建记号对象并返回
            if self.current_char == '-':  # 如果当前字符是减号
                self.advance()  # 跳到下一字符
                return Token(MINUS, '-')  # 创建记号对象并返回
            if self.current_char == '*':
                self.advance()  # 跳到下一字符
                return Token(MUL, '*')  # 创建记号对象并返回
            if self.current_char == '/':  # 当前字符为斜杠时
                self.advance()  # 提取下一字符
                return Token(FLOAT_DIV, '/')  # 返回浮点数除法记号
            if self.current_char == '(':
                self.advance()  # 跳到下一字符
                return Token(LPAREN, '(')  # 创建记号对象并返回
            if self.current_char == ')':
                self.advance()  # 跳到下一字符
                return Token(RPAREN, ')')  # 创建记号对象并返回
            if self.current_char == '{':
                self.advance()  # 跳到下一字符
                return Token(LBRACE, '{')  # 创建记号对象并返回
            if self.current_char == '}':
                self.advance()  # 跳到下一字符
                return Token(RBRACE, '}')  # 创建记号对象并返回
            if self.current_char.isalpha():  # 如果当前字符是字母
                result = self._id()  # 调用方法返回保留字或赋值名称的记号
                # print(result)
                return result
            if self.current_char == ':' and self.peek() == '=':  # 如果当前字符是“:”，并且下一个字符是“=”。
                self.advance()  # 提取下一个字符
                self.advance()  # 提取下一个字符
                return Token(ASSIGN, ':=')  # 返回赋值符的记号
            if self.current_char == ';':  # 如果当前字符是分号
                self.advance()  # 提取下一个字符
                return Token(SEMI, ';')  # 返回分号记号
            if self.current_char == '.':  # 如果当前字符是点
                self.advance()  # 提取下一个字符
                return Token(DOT, '.')  # 返回点记号
            if self.current_char == ':':  # 如果当前字符是冒号
                self.advance()  # 提取下一个字符
                return Token(COLON, ':')  # 返回冒号记号
            if self.current_char == ',':  # 如果当前字符是逗号
                self.advance()  # 提取下一个字符
                return Token(COMMA, ',')  # 返回逗号记号
            if self.current_char == '\"':
                self.advance()  # 提取下一个字符
                result = self.long_string()
                # print(result)
                return result
            if self.current_char == '\'':
                self.advance()  # 提取下一个字符
                result = self.short_string()
                # print(result)
                return result
            if self.current_char == '\\': # 换行
                self.advance()  # 提取下一个字符
                continue
            if self.current_char == '=':
                self.advance()  # 跳到下一字符
                return Token(EQUAL, '=')  # 创建记号对象并返回
            self.error()  # 如果以上都不是，则抛出异常。
        return Token(EOF, None)  # 遍历结束返回结束标识创建的记号对象

    def analyse(self):  # 进行词法分析, 注意：不能与语法分析同时进行
        self.tokens = []    # 保存所有的词法单元
        while self.current_char is not None:
            token = self.get_next_token()
            self.tokens.append(token)
            print(token)
        return self.tokens

##############################################
#  Parser   语法分析器                        #
##############################################
class AST(object):
    pass

class Comment(AST):
    def __init__(self, comments):
        self.comments = comments

# key name or function name
class Identifier(AST):  # 添加变量节点
    def __init__(self, token):
        self.token = token  # 记号
        self.name = token.value  # 变量值

class KeyVal(AST):  # 添加键值对节点
    def __init__(self, left, token, right):
        self.left  = left       # 左值为键
        self.token = token      # 冒号
        self.right = right      # 右值为值

class Call(AST):    # 添加函数声明节点
    def __init__(self, name, arguments, dictionary = None, comments = None):
        self.name = name                # 函数名
        self.arguments = arguments      # 函数参数
        self.dictionary = dictionary    # 函数域
        self.comments = comments        # 注释

class Atom(AST):    # 添加原子节点
    def __init__(self, atom):
        self.atom = atom

class Argument(AST):    # 添加函数参数节点
    def __init__(self, arguments):
        self.arguments = arguments

class Dictionary(AST):  # 添加函数域节点
    def __init__(self, dictionary):
        self.dictionary = dictionary

class String(AST):      # 添加字符串节点
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Num(AST):     # 添加数字节点
    def __init__(self, token):
        self.token = token
        self.value = token.value

class BinOp(AST):   # 添加操作符节点
    def __init__(self,left,op,right):
        self.left=left                  # 操作符左侧
        self.token = self.op = op       # 操作符
        self.right = right              # 操作符右侧

class UnaryOp(AST):     # 添加一元操作符节点
    def __init__(self,op,expr):
        self.token = self.op = op       # 操作符
        self.expr = expr                # 表达式

class Compound(AST):  # 添加复合语句节点
    def __init__(self):
        self.children = []  # 子节点列表

class Assign(AST):  # 添加赋值语句节点
    def __init__(self, left, operator, right):
        self.left = left  # 变量名称
        self.token = self.operator = operator  # 记号和赋值符号
        self.right = right  # 右侧表达式

class Variable(AST):  # 添加变量节点
    def __init__(self, token):
        self.token = token  # 记号
        self.name = token.value  # 变量值

class NoOp(AST):  # 添加空语句节点
    pass  # 无内容

class Type(AST):  # 定义类型节点
    def __init__(self, token):
        self.token = token
        self.name = token.value

class ProcedureDecl(AST):  # 添加过程声明节点
    def __init__(self, name, block_node):
        self.name = name  # 名称
        self.block_node = block_node  # 块节点

class VarDecl(AST):  # 定义变量声明节点
    def __init__(self, var_node, type_node):  # 变量声明由变量和类型组成
        self.var_node = var_node
        self.type_node = type_node

class Block(AST):  # 定义语句块节点
    def __init__(self, declarations, compound_statement):  # 语句块由声明和符合语句组成
        self.declarations = declarations
        self.compound_statement = compound_statement

class Program(AST):  # 定义程序节点
    def __init__(self, name, block):  # 程序由名称和语句块组成
        self.name = name
        self.block = block

class Parser:  #语法分析器
    def __init__(self, lexer):  # 定义构造方法获取用户输入的表达式
        self.lexer = lexer  # 词法对象
        self.current_token = self.lexer.get_next_token() # 语法分析器初始化
        self.remember_stack = []    # 暂时保存当前的词法单元

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

    def breakpoint(self): # 记录当前的词法单元
        breakpoint = self.lexer.mark()     # add breakpoint
        self.remember_stack.append(self.current_token)
        caller = traceback.extract_stack()
        # print("%s %s invoke" % (caller[-2], caller[-2][2]))
        # print("%s invoke" % (caller[-2][2]))
        # print("before:", breakpoint, self.current_token)
        return breakpoint

    def recall(self): # 回退之前的词法单元
        breakpoint = self.lexer.release()
        self.current_token = self.remember_stack.pop(-1)
        caller = traceback.extract_stack()
        # print("%s %s invoke" % (caller[-2], caller[-2][2]))
        # print("%s invoke" % (caller[-2][2]))
        # print("after: ", breakpoint, self.current_token)
        return breakpoint

    # detect next k token
    def detect(self, k): # 往前看第k个词法单元
        self.breakpoint()
        last_token = None
        for i in range(k):
            if self.lexer.position < len(self.lexer.text): # I don't know whether this code is must
                last_token = self.lexer.get_next_token()
        self.recall()
        return last_token

    # recall and speculate
    def speculate(self, production, follow_set = None): # 预测前面的产生式
        follow_token = None
        func = getattr(self, production, None)
        if not func:
            raise Exception(f"No existing this production: {production}")
        need_continue = True
        self.breakpoint()
        try:
            # print(self.current_token)
            # print(self.lexer.position)
            func()
            follow_token = self.current_token
            # print(self.current_token)
            # print(self.lexer.text[:self.lexer.position])
        except:
            need_continue = False
        self.recall()

        if follow_set and follow_token:
            if follow_token.type != follow_set:
                need_continue = False
        return need_continue

    def is_speculating(self):
        if self.remember_stack:
            return True
        return False

    def factor(self):          #语法分析器最底层结构：整数或括号
        token = self.current_token  # 获取记号
        if (token.type in (PLUS,MINUS)):
            self.eat(token.type)
            node=UnaryOp(token,self.factor())
            return node
        if (token.type in (INTEGER_CONST,REAL_CONST)):   # 整数
            self.eat(token.type)
            return Num(token)  # 返回数字节点对象
        elif (token.type == LPAREN):  # 左括号
            self.eat(LPAREN)
            node = self.expr()              # 求出括号里面的AST树
            self.eat(RPAREN)                # 右括号
            return node                     # 返回括号内的AST树
        else:  # 新增变量因子
            node = self.variable()  # 获取变量节点
            return node  # 返回变量节点

    def term(self):           #语法分析器中间层结构：乘除
        node=self.factor()    # 获取第一个数字树,如没有乘除法，将直接返回一个代表数字的叶节点树
        while (self.current_token.type in (MUL,INTEGER_DIV,FLOAT_DIV)):
            token = self.current_token
            self.eat(token.type)
            # 生成新的树：把目前已经获取到的乘除法树整体做为左子树，起到连续乘除的作用
            node = BinOp(left=node, op=token, right=self.factor())
            # 新的树以取得新的数字或括号内的树为右子树
        return node

    def expr(self):          #语法分析器最高层结构：加减
        node=self.term()     # 获取第一段乘除
        while (self.current_token.type in (PLUS,MINUS)):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            if token.type == MINUS:
                self.eat(MINUS)
            # 生成新的树：把目前已经获取到的加减法树整体做为左子树，起到连续加减的作用
            node = BinOp(left=node, op=token, right=self.term())
            # 新的树以取得新的数字或括号内的树为右子树
        return node

    def variable(self):  # 添加获取变量节点的方法
        node = Variable(self.current_token)  # 获取变量节点
        self.eat(ID)  # 验证变量名称
        return node  # 返回变量节点

    def empty(self):  # 添加获取空语句节点的方法
        return NoOp()  # 返回空语句节点

    def assignment_statement(self):  # 添加获取赋值语句节点的方法
        left = self.variable()  # 获取变量名称节点
        token = self.current_token  # 获取当前记号
        self.eat(ASSIGN)  # 验证赋值符
        right = self.expr()  # 获取表达式节点
        node = Assign(left, token, right)  # 组成赋值语句节点
        return node  # 返回赋值语句节点

    def statement(self):  # 添加获取语句节点的方法
        if self.current_token.type == BEGIN:  # 如果遇到BEGIN，说明包含复合语句。
            node = self.compound_statement()  # 获取复合语句节点
        elif self.current_token.type == ID:  # 如果遇到一个名称，说明是赋值语句。
            node = self.assignment_statement()  # 获取赋值语句节点
        else:  # 否则就是空语句
            node = self.empty()  # 返回空语句节点
        return node  # 返回语句节点

    def statement_list(self):  # 添加获取语句列表节点的方法
        node = self.statement()  # 获取第一条语句节点
        nodes = [node]  # 添加第一条语句节点到列表
        while self.current_token.type == SEMI:  # 如果遇到分号
            self.eat(SEMI)  # 验证分号
            nodes.append(self.statement())  # 添加下一条语句节点到列表
        if self.current_token.type == ID:  # 如果只遇到一个名称而非语句
            self.error()  # 抛出异常
        return nodes  # 返回语句节点列表

    def compound_statement(self):  # 添加获取复合语句节点的方法
        self.eat(BEGIN)
        nodes = self.statement_list()  # 包含节点为语句列表
        self.eat(END)

        root = Compound()  # 创建复合语句节点对象
        root.children = nodes  # 将语句节点列表添作为复合语句节点的子节点列表
        return root  # 返回复合语句节点对象

    def type_spec(self):  # 构造变量类型节点的方法
        token = self.current_token  # 获取当前记号
        if token.type == INTEGER:  # 如果是整数类型
            self.eat(INTEGER)  # 验证整数记号
        else:  # 否则
            self.eat(REAL)  # 验证实数记号
        node = Type(token)  # 创建类型节点
        return node  # 返回类型节点

    def declarations(self):  # 构造声明节点的方法
      declarations = []  # 声明节点包含多个变量声明节点
      while True:  # 遍历声明
        if self.current_token.type == VAR:  # 如果当前记号为变量
            self.eat(VAR)  # 验证记号
            while self.current_token.type == ID:  # 遍历变量名称
                declarations.extend(self.variable_declaration())  # 声明列表中添加变量声明
                self.eat(SEMI)  # 验证分号
        elif self.current_token.type == PROCEDURE:  # 当前记号类型是过程时
            self.eat(PROCEDURE)  # 验证过程类型
            procedure_name = self.current_token.value  # 获取过程名称
            self.eat(ID)  # 验证过程名称
            self.eat(SEMI)  # 验证分号
            block_node = self.block()  # 获取过程中的块
            procedure_decl = ProcedureDecl(procedure_name, block_node)  # 由过程名称和块组成过程声明对象
            declarations.append(procedure_decl)  # 声明列表末尾添加新的过程声明
            self.eat(SEMI)  # 验证分号
        else:  # 否则
            break  # 结束声明遍历
      return declarations

    def variable_declaration(self):  # 构造变量声明节点的方法
        var_nodes = [Variable(self.current_token)]  # 第一个变量声明节点添加到变量声明节点列表
        self.eat(ID)  # 验证变量名称记号
        while self.current_token.type == COMMA:  # 遍历逗号
            self.eat(COMMA)  # 验证逗号
            var_nodes.append(Variable(self.current_token))  # 添加变量节点到变量节点列表
            self.eat(ID)  # 验证变量名称记号
        self.eat(COLON)  # 验证冒号
        type_node = self.type_spec()  # 一组变量声明的类型节点
        var_declarations = [VarDecl(var_node, type_node) for var_node in var_nodes]  # 生成变量声明列表
        return var_declarations  # 返回变量声明节点列表

    def block(self):  # 构造块节点的方法
        declarations = self.declarations()
        compound_statement = self.compound_statement()
        node = Block(declarations, compound_statement)  # 块节点由声明节点和符合语句节点组成
        return node

    def program(self):
        self.eat(PROGRAM)  # 验证程序开始标记
        var_node = self.variable()  # 获取变量节点
        program_name = var_node.name  # 获取程序名称
        self.eat(SEMI)  # 验证分号
        block_node = self.block()  # 获取块节点
        node = Program(program_name, block_node)  # 创建程序节点
        self.eat(DOT)  # 验证程序结束符号
        return node  # 返回程序节点

    def parser(self):
        node = self.program()  # 获取程序所有节点
        if self.current_token.type != EOF:  # 如果当前不是文件末端记号
            self.error()  # 抛出异常
        return node  # 返回程序节点

# with recall
class AdvancedParser(Parser):
    def parser(self):
        node = self.stat()  # 获取程序所有节点
        if self.current_token.type != EOF:  # 如果当前不是文件末端记号
            self.error()  # 抛出异常
        return node  # 返回程序节点

    # without memory
    # stat      ::= list EOF | assign EOF
    # assign    ::= list "=" list
    # list      ::= "(" elements ")"
    # elements  ::= element (',' element)*
    # element   ::= ID '=' ID | ID | list
    def stat(self):
        if self.speculate("list_display", follow_set = EOF):
            self.list_display()
        elif self.speculate("assign", follow_set = EOF):
            self.assign()
        else:
            self.error()

    # with memory
    # stat      ::= list EOF | list "=" list
    def stat(self):
        if self.speculate("_list_display", follow_set = EOF):
            self.list_display()
        elif self.speculate("_list_display"):
            self.list_display()
            self.eat(EQUAL)
            self.list_display()
        else:
            self.error()

    def assign(self):
        self.list_display()
        self.eat(EQUAL)
        self.list_display()

    # production with memory
    def _list_display(self):
        try:
            getattr(self, "list_memory")
        except:
            self.list_memory = []
        # print(self.list_memory)
        failed = False
        start_token = (self.lexer.position, self.current_token)
        if self.is_speculating() and self.already_parsed_production(self.list_memory):
            return
        try:
            self.list_display()
        except:
            failed = True
        finally:
            if self.is_speculating():
                self.memoize(self.list_memory, start_token, failed)

    def already_parsed_production(self, memoization):
        if not memoization:
            return False
        memo = memoization.pop(-1)
        print(f"Parsed list before at position {self.lexer.position}, token {self.current_token}")
        if memo[-1][0] == -1:
            raise Exception()
        print(f"Skip ahead to token position {memo[-1][0]}, token {memo[-1][-1]}")
        # recall pointer
        self.lexer.position = memo[-1][0]
        self.current_token = memo[-1][-1]
        return True

    def memoize(self, memoization, start_token, failed):
        # (position, token)
        # -1 is fail, >0 is stop position
        stop_token = (-1, self.current_token) if failed else (self.lexer.position, self.current_token)
        memoization.append((start_token, stop_token))

    def list_display(self):
        self.eat(LPAREN)
        # if self.current_token in [ID, LPAREN]:
        self.elements()
        self.eat(RPAREN)

    def elements(self):
        self.element()
        while self.current_token.type == COMMA:
            self.eat(COMMA)
            self.element()

    def element(self):
        # if self.detect(1) and self.detect(2) and \
        if self.detect(1).type != EOF and self.detect(2).type != EOF and \
            self.current_token.type == ID and self.detect(1).type == EQUAL and self.detect(2).type == ID:
            self.eat(ID)
            self.eat(EQUAL)
            self.eat(ID)
        elif self.current_token.type == ID:
            self.eat(ID)
        elif self.speculate("list_display"):
            self.list_display()
        else:
            self.error()

# @Grammar: Liberty
# <start>           ::= <key_datum>
# <key_datum>       ::= <atom> <key_tail>
# <key_tail>        ::= ":" <atom> ";" | "(" <argument_list>? ")" <dict_tail>
# <dict_tail>       ::= ";" | <dict_display>
# <dict_display>    ::= "{" <key_datum>+ "}"
# <argument_list>   ::= <position_item> ("," position_item)*
# <position_item>   ::= <atom>
# <atom>            ::= ID | NUM | STRING | <expression>
# <expression>      ::= ... (expression BNF refer web)
class LibertyParser(Parser): # 继承解析<expression>的方法
    def __init__(self, lexer):  # 定义构造方法获取用户输入的表达式
        self.lexer = lexer  # 词法对象
        self.current_token = self.lexer.get_next_token() # 语法分析器初始化
        # header comment
        while self.current_token.type == COMMENT:
            self.current_token = self.lexer.get_next_token()
        self.remember_stack = []    # 暂时保存当前的词法单元

    def parser(self):
        node = self.key_datum()  # 获取程序所有节点
        if self.current_token.type != EOF:  # 如果当前不是文件末端记号
            self.error()  # 抛出异常
        return node  # 返回程序节点

    # <atom> ::= ID | NUM | STRING | <expression>
    def atom(self):
        node = None
        token = self.current_token
        if self.current_token.type == ID:
            self.eat(token.type)
            node = Identifier(token)
        elif self.current_token.type in [INTEGER_CONST, REAL_CONST]:
            self.eat(token.type)
            node = Num(token)
        elif self.current_token.type == STRING:
            self.eat(token.type)
            node = String(token)
        # expr first set
        # 求<expr> first集
        elif self.current_token.type in self.expr_first_set():
            node = self.expr()
        node = Atom(node)
        return node

    def identifier(self):  # 添加获取ID节点的方法
        node = Identifier(self.current_token)  # 获取ID节点
        self.eat(ID)  # 验证ID名称
        return node  # 返回ID节点

    def comment(self):
        node = None
        if self.current_token.type == COMMENT:
            comments = []
            while self.current_token.type == COMMENT:
                comments.append(self.current_token.value)
                self.eat(COMMENT)
            node = Comment(comments)
        return node

    # <key_datum> ::= <atom> <key_tail>
    # <key_tail>  ::= ":" <atom> ";" | "(" <argument_list>? ")" <dict_tail>
    # <dict_tail> ::= ";" | <dict_display>
    def key_datum(self):
        node = self.identifier()
        if self.current_token.type == COLON:        # 键值对文法
            token = self.current_token
            self.eat(COLON)
            node = KeyVal(left = node, token = token, right = self.atom()) # 例如：key1 : value1 ;
            self.eat(SEMI)
            self.comment()
        elif self.current_token.type == LPAREN:     # 函数文法
            self.eat(LPAREN)
            arguments = None                        # 未定义函数参数，例如：bus() ...
            # position_item/Atom first set
            if self.current_token.type in self.atom_first_set():    # 如果匹配到position_item的first集，说明有定义函数参数
                arguments = self.argument_list()    # 定义函数参数，例如：bus(A) ...
            self.eat(RPAREN)
            if self.current_token.type == SEMI:     # 未定义函数域, 例如：bus(A) ;
                node = Call(name = node, arguments = arguments)
                self.eat(SEMI)
                self.comment()
            elif self.current_token.type == LBRACE: # 定义函数域，例如：bus(A) {...}
                self.eat(LBRACE)
                # self.comment()
                node = Call(
                    name = node,
                    arguments = arguments,
                    comments = self.comment(),
                    dictionary = self.dict_display()
                    )
                self.comment()
        return node

    # <dict_display> ::= "{" <key_datum>+ "}"
    def dict_display(self):     # 函数域
        # self.eat(LBRACE)
        dict_list = []
        # dict_list.append(self.key_datum())
        while True:     # 在函数域中至少有一个函数定义或者键值对定义
            if self.current_token.type == ID:
                dict_list.append(self.key_datum())
            elif self.current_token.type == RBRACE:
                break
            else:
                self.error()
        self.eat(RBRACE)
        return Dictionary(dict_list)

    # <argument_list> ::= <position_item> ("," position_item)*
    def argument_list(self):    # 函数参数列表，至少有一个函数参数，函数参数间用逗号分隔
        arguments = []
        arguments.append(self.position_item())
        while self.current_token.type == COMMA:
            self.eat(COMMA)
            if self.current_token.type in self.atom_first_set():
                arguments.append(self.position_item())
            else:
                self.error()
        return Argument(arguments)

    # <position_item> ::= <atom>
    def position_item(self):
        return self.atom()

    # 有关“求first集”的内容需要查阅《编译原理》
    # first set
    # atom = ID + Num + String + expression
    def atom_first_set(self):
        return [ID, INTEGER_CONST, STRING, REAL_CONST] + self.expr_first_set()

    def expr_first_set(self):
        return [MINUS, PLUS, LPAREN]

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

##############################################
#  Semantic Analyzer  语义分析器              #
##############################################
class Symbol:  # 添加符号类
    def __init__(self, name, symbol_type=None):
        self.name = name  # 符号名称
        self.symbol_type = symbol_type  # 符号类型

class BuiltinTypeSymbol(Symbol):  # 添加内置类型符号类
    def __init__(self, name):
        super().__init__(name)  # 调用基类构造函数初始化

    def __str__(self):
        return self.name  # 返回符号名称

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}')"  # 输出类名和符号名称

class VarSymbol(Symbol):  # 添加变量符号类
    def __init__(self, name, symbol_type):
        super().__init__(name, symbol_type)  # 调用基类构造函数初始化

    def __str__(self):
        return f"<{self.__class__.__name__}(name='{self.name}':type='{self.symbol_type}')>"  # 输出类名、符号名称和类型

    __repr__ = __str__

class SymbolTable:  # 添加符号表类
    def __init__(self):
        self._symbols = OrderedDict()  # 存储符号的有序字典
        self._init_builtins()  # 初始化内置类型

    def _init_builtins(self):  # 定义初始化内置类型的方法
        self.insert(BuiltinTypeSymbol('INTEGER'))  # 通过insert()方法存入内置类型符号
        self.insert(BuiltinTypeSymbol('REAL'))  # 通过insert()方法存入内置类型符号

    def __str__(self):
        symtab_header = '符号表中的内容：'
        lines = [symtab_header, '-' * len(symtab_header) * 2]  # 头部标题与分割线存入打印内容的列表
        lines.extend([f'{key:8}: {value}' for key, value in self._symbols.items()])  # 符号表内容合并到打印内容列表
        s = '\n'.join(lines)  # 以换行符连接每个列表元素组成字符串
        return s  # 返回打印内容

    __repr__ = __str__

    def insert(self, symbol):  # 添加存入符号的方法
        print(f'存入：{symbol}')
        self._symbols[symbol.name] = symbol  # 以符号名称为键存入符号

    def lookup(self, name):  # 添加查询符号的方法
        print(f'查询：{name}')
        symbol = self._symbols.get(name)
        return symbol

"""
# @web: https://blog.csdn.net/Dontla/article/details/118970762
# 如何遍历树以正确评估该树表示的表达式？您可以通过使用后序遍历（深度优先遍历的一种特殊情况）
# 来实现这一点，它从根节点开始并从左到右递归访问每个节点的子节点。后序遍历尽可能快地访问远离根的节点。
def visit(node):
    # for every child node from left to right
    for child in node.children:
        visit(child)
    <<post-order actions>>
# 我们要为解释器使用后序遍历的原因是，首先，我们需要评估树中较低的内部节点，
# 因为它们代表具有更高优先级的运算符；其次，我们需要在应用运算符之前评估运算符的操作数到那些操作数。

# 为了完整起见，我将提到深度优先遍历的三种类型：前序遍历、中序遍历和后序遍历。
# 遍历方法的名字来自你在访问代码中放置动作的地方：
def visit(node):
    <<pre-order actions>>
    left_val = visit(node.left)
    <<in-order actions>>
    right_val = visit(node.right)
    <<post-order actions>>
"""
class SemanticAnalyzer(NodeVisitor):  # 添加语义分析器
    def __init__(self):
        self.symbol_table = SymbolTable()  # 创建符号表

    def visit_Program(self, node):  # 添加与访问变量声明相关的访问方法
        self.visit(node.block)

    def visit_Block(self, node):  # 添加与访问变量声明相关的访问方法
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_VarDecl(self, node):  # 添加访问变量声明节点方法
        symbol_type  = node.type_node.name  # 获取变量类型名称
        self.symbol_table.lookup(symbol_type)

        var_name = node.var_node.name
        if self.symbol_table.lookup(var_name) is not None:  # 查询变量名称，如果存在变量信息
            raise Exception(f'错误：发现重复的标识符：{var_name}')  # 抛出异常
        var_symbol = VarSymbol(var_name, symbol_type)  # 创建变量符号对象
        self.symbol_table.insert(var_symbol)  # 变量符号对象添加到符号表

    def visit_Compound(self, node):  # 添加与访问变量声明相关的访问方法
        for child in node.children:
            self.visit(child)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Assign(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Variable(self, node):
        var_name = node.name
        var_symbol = self.symbol_table.lookup(var_name)
        if var_symbol is None:  # 如果变量未声明
            raise NameError(f'引用了不存在的标识符：{repr(var_name)}')  # 抛出语义错误

    def visit_Type(self, node):
        pass

    def visit_Num(self, node):
        pass

    def visit_ProcedureDecl(self, node):
        pass

    def visit_NoOp(self, node):  # 添加与访问变量声明相关的访问方法
        pass

    def visit_Identifier(self, node):
        pass

    # node is KeyVal instance
    def visit_KeyVal(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Call(self, node):
        self.visit(node.name)
        # print(node.argument)
        if node.arguments is not None:
            # self.visit(node.argument)
            # for argument in node.argument:
            #     self.visit(argument)
            self.visit(node.arguments)
        if node.dictionary is not None:
            # for dictionary in node.dictionary:
            #     self.visit(dictionary)
            self.visit(node.dictionary)

    def visit_Atom(self, node):
        pass

    def visit_Argument(self, node):
        if len(node.arguments) == 1:
            # return Atom
            return self.visit(node.arguments[0])
        # return list
        for arg in node.arguments:
            self.visit(arg)

    def visit_Dictionary(self, node):
        for dic in node.dictionary:
            self.visit(dic)

    def visit_String(self, node):
        pass

    def visit_Comment(self, node):
        pass


##############################################
#  Interpreter  解释器                        #
##############################################
class Interpreter(NodeVisitor):
    def __init__(self, tree):  # 修改构造方法
        self.tree = tree  # 获取参数AST
        self.GLOBAL_MEMORY = OrderedDict()  # 创建全局存储字典

    #   以下为AST各节点的遍历方法--------------------
    def visit_BinOp(self, node):  # 访问二元运算符类型节点的方法
        if node.op.type == PLUS:  # 如果操作符类型是加法
            # 分别访问左侧和右侧的记号，将获取的值进行加法运算，并返回结果。
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == INTEGER_DIV:
            return self.visit(node.left) // self.visit(node.right)
        elif node.op.type == FLOAT_DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):  # 访问数字类型节点的方法
        return node.value

    def visit_UnaryOp(self, node):#一元运算符类型节点的方法
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def visit_Compound(self, node):  # 访问复合语句节点
        for child in node.children:  # 遍历复合语句节点的子节点
            self.visit(child)  # 访问子节点

    def visit_Assign(self, node):  # 访问赋值语句节点
        var_name = node.left.name  # 获取变量名称
        self.GLOBAL_MEMORY[var_name] = self.visit(node.right)  # 以变量名称为键添加变量值到符号表

    def visit_Variable(self, node):  # 访问变量节点
        var_name = node.name  # 获取变量名称
        value = self.GLOBAL_MEMORY.get(var_name)  # 获取变量值
        if value is None:  # 如果没有返回值（变量不存在）
            raise NameError(f'错误的标识符：{repr(var_name)}')  # 抛出异常
        else:  # 否则
            return value  # 返回变量值

    def visit_NoOp(self, node):  # 访问空语句节点
        pass  # 无操作

    def visit_Program(self, node):  # 添加访问程序的方法
        self.visit(node.block)  # 访问语句块

    def visit_Block(self, node):  # 添加访问语句块的方法
        for declaration in node.declarations:  # 遍历声明列表
            self.visit(declaration)  # 访问声明
        self.visit(node.compound_statement)  # 访问复合语句

    def visit_VarDecl(self, node):  # 添加访问变量声明的方法
        pass  # 无需处理

    def visit_ProcedureDecl(self, node):  # 添加访问过程声明的方法
        pass  # 暂不处理

    def visit_Type(self, node):  # 添加访问类型的方法
        pass  # 无需处理

    def visit_Identifier(self, node):   # 添加访问ID的方法
        return node.name

    def visit_KeyVal(self, node):   # 添加访问键值对的方法
        return {
            self.visit(node.left) : self.visit(node.right),
            }

    def visit_Comment(self, node):
        return "\n".join(node.comments).strip()

    def visit_Call(self, node):     # 添加访问函数定义的方法
        name = self.visit(node.name)
        # arguments = []
        arguments = None
        if node.arguments is not None:      # 可能没有函数参数
            arguments = self.visit(node.arguments)
        # dictionaries = []
        dictionaries = None
        if node.dictionary is not None:     # 可能没有函数域
            # for dictionary in node.dictionary:
            #     dictionaries.append(self.visit(dictionary))
            dictionaries = self.visit(node.dictionary)
        comments = None
        if node.comments is not None:     # 可能没有注释
            comments = self.visit(node.comments)
        return {
            "_name"          : name,            # 函数名
            "_argument"      : arguments,       # 函数参数
            "_dictionary"    : dictionaries,    # 函数域
            "_comment"       : comments,        # 注释
        }

    def visit_Atom(self, node):     # 添加访问原子的方法
        return self.visit(node.atom)

    def visit_Argument(self, node):     # 添加访问函数参数的方法
        if len(node.arguments) == 1:    # 只有一个函数参数
            # return Atom
            return self.visit(node.arguments[0])
        # return list
        arguments = []
        for arg in node.arguments:      # 多个函数参数
            arguments.append(self.visit(arg))
        if not arguments:               # 无函数参数
            return None
        return arguments

    def visit_Dictionary(self, node):     # 添加访问函数域的方法
        dictionary = []
        for dic in node.dictionary:         # 多个函数域
            dictionary.append(self.visit(dic))
        if not dictionary:                  # 函数定义中未定义函数域
            return None
        return dictionary

    def visit_String(self, node):           # 添加访问字符串的方法
        return node.value
    #  以上为AST各节点的遍历方法--------------------

    def interpret(self):  # 执行解释的方法
        tree = self.tree  # 获取AST
        if tree is None:  # 如果AST不存在
            return ''  # 返回空字符串
        return self.visit(tree)  # 否则访问AST

# 只能搜索到timing()
def search_lib(data, **kwargs):
    copy_kwargs = deepcopy(kwargs)
    for key, value in kwargs.items():
        if isinstance(data, dict):
            if key in data["_name"] and (value is None or value in data["_argument"]):
                copy_kwargs.pop(key)
                return search_lib(data["_dictionary"], **copy_kwargs)
        elif isinstance(data, list):
            result = []
            for kv in data:
                if "_dictionary" in kv:
                    if key in kv["_name"] and (value is None or value in kv["_argument"]):
                        if key in copy_kwargs:
                            copy_kwargs.pop(key)
                        result.append(search_lib(kv["_dictionary"], **copy_kwargs))
                        # return search_lib(kv["_dictionary"], **copy_kwargs)
                else:
                    if key in kv:
                        return kv[key]
            # 出现多个timing()
            if len(result) == 1:
                return result[0]
            else:
                return result
    if not copy_kwargs:
        return data
    return None

def get_template_name(timing_data, table):
    for record in timing_data:
        if "_name" in record and "_dictionary" in record:
            if record["_name"] == table:
                return record["_argument"]
    return None

def get_timing(
        liberty_data,
        *,
        library=None,
        cell=None,
        port=None,
        timing_type=None,
        related_pin=None,
        timing=None
    ):
    cell_data = search_lib(liberty_data, library=library, cell=cell)
    if not cell_data:
        return None
    if not port:
        return cell_data

    port_data = search_lib(cell_data, pin=port)
    if not port_data:
        port_data = search_lib(cell_data, bus=port)
    if not port_data:
        return None
    if not timing:
        return port_data

    timing_data = search_lib(port_data, timing=None)
    if not timing_data:
        return None

    for one_timing_data in timing_data:
        if isinstance(one_timing_data, dict):
            if not timing_type and related_pin:
                related_pin_value = search_lib(timing_data, related_pin=None)
                if related_pin_value != related_pin:
                    return None
            elif timing_type and not related_pin:
                timing_type_value = search_lib(timing_data, timing_type=None)
                if timing_type_value != timing_type:
                    return None
            break
        elif isinstance(one_timing_data, list):
            if not timing_type and related_pin:
                related_pin_value = search_lib(one_timing_data, related_pin=None)
                if related_pin_value == related_pin:
                    timing_data = one_timing_data
                    break
            elif timing_type and not related_pin:
                timing_type_value = search_lib(one_timing_data, timing_type=None)
                if timing_type_value == timing_type:
                    timing_data = one_timing_data
                    break
    else:
        return None

    table_data = search_lib(timing_data, **{timing:None})
    if not table_data:
        None
    # return table_data
    values = table_data[0]["_argument"]
    matrix_or_list = [re.split(r"\s*,\s*", row) if "," in row else row for row in values]
    return matrix_or_list

def main():
    text = '''
PROGRAM SymTab6[12];
"long_string"
'short_string'
{test}
/*sdfsfsdf*/
   var x, y : integer; /*sdfsfsdf*/
   var y : real;
begin
   x := x + y;
END.
/*wei*/'''

    text = r'''
/*wei*/
/*wei*/
library (MC) {
    revision : 1.0;
    nom_voltage : -88e-1;
    lut_table_template(CELL_DELAY) {
        variable_1 : input_net_transition;
        variable_2 : total_output_net_capacitance;
        index_1 ("0.004,0.05,0.1,0.2,0.5,0.75,1.0");
        index_2 ("0.001,0.02,0.05,0.1,0.25,0.3,0.35");
    }
    lut_table_template(CONSTRAINT) {
        variable_1 : related_pin_transition;
        variable_2 : constrained_pin_transition;
        index_1 ("0.004,0.05,0.1,0.2,0.5,0.75,1.0");    /* comment */
        index_2 ("0.004,0.05,0.1,0.2,0.5,0.75,1.0");
    }
    cell (cell_name) {
        bus (A[1]) {
            bus_type        : address_bus;
            direction       : input;    /* comment */
            capacitance     : 0.010971;
            max_transition  : 1.0;
            switch_pin      : false;

            related_power_pin   : "VDD";
            related_ground_pin  : "VSS";

            timing() {
            /* comment */
                timing_type     : setup_rising;
                related_pin     : "CK";
                when            : "!CEB";
                rise_constraint(CONSTRAINT) {
                    values("0.0472,0.0521,0.0472,0.0521", \
                        "0.04,0.0521,0.0472,0.0521");
                }
            }
            timing() {
            /* comment */
                timing_type     : setup_hold;
                related_pin     : "CK";
                when            : "!CEB";
                rise_constraint(CONSTRAINT) {
                    values("0.0472,0.0521,0.0472,0.0521", \
                        "0.04,0.0521,0.0472,0.0521");
                }
            }
            interface_timing : true;
            dont_use         : true;
        }

        pin(EMCE) {
            direction : input;
            capacitance : 0.001985;
            max_transition : false;
            switch_pin : false;
            related_power_pin : "VDD";
            related_ground_pin : "VSS";
        }
    }
}
/*wei*/'''
    print(text)
    print('\n开始词法分析...')
    lexer = Lexer(text)
    # lexer.analyse()

    if 1:
        print('\n开始语法分析...')
        parser = LibertyParser(lexer)
        tree = parser.parser()

        print('\n开始语义分析...')
        semantic_analyzer  = SemanticAnalyzer()
        semantic_analyzer.visit(tree)
        # print(semantic_analyzer.symbol_table)

        print('\n开始解释代码...')
        interpreter = Interpreter(tree)
        result = interpreter.interpret()
        pprint(result)

    # pprint(search_lib(result, library="MC", cell="cell_name", bus="A[1]", timing=None))
    if 0:
        pprint(search_lib(result, library="MC", revision=None))
        pprint(search_lib(result, library="MC", cell="cell_name"))
        pprint(search_lib(result, library="MC", cell="cell_name", bus="A[1]"))
        pprint(search_lib(result, library="MC", cell="cell_name", bus="A[1]", timing=None))
        pprint(search_lib(result, library="MC", cell="cell_name", bus="A[1]", timing=None, timing_type="setup_hold"))
        # pprint(search_lib(result, library="MC", cell="cell_name", bus="A[1]", timing=None, rise_constraint="CONSTANT"))
        pprint(search_lib(result, library="MC", cell="cell_name", bus="A[1]", timing=None, rise_constraint=None))
        pprint(search_lib(result, library="MC", cell="nothing", bus="A[1]", timing=None, rise_constraint=None))
        pprint(search_lib(result, library="MC", cell="cell_name", bus="A[1]", timing=None, cell_rise=None))
        pprint(search_lib(result, library="MC", lut_table_template="CONSTRAINT"))
        pprint(search_lib(result, library="MC", lut_table_template="CELL_DELAY"))
        pprint(search_lib(result, library="MC", lut_table_template="nothing"))
        pprint(search_lib(search_lib(result, library="MC", cell="cell_name"), bus="A[1]"))
        cell = search_lib(result, library="MC", cell="cell_name")
        if search_lib(cell, pin="A[1]"):
            print("port")
        elif search_lib(cell, bus="A[1]"):
            print("bus")
        else:
            print(None)
        template_name = get_template_name(search_lib(result, library="MC", cell="cell_name", bus="A[1]", timing=None), table="rise_constraint")
        pprint(search_lib(result, library="MC", lut_table_template=template_name))

    if 0:
        timing = get_timing(result, library="MC", cell="cell_name")
        pprint(timing)
        timing = get_timing(result, library="MC", cell="cell_name", port="A[1]")
        pprint(timing)
        timing = get_timing(result, library="MC", cell="cell_name", port="A[1]", timing_type="setup_rising", timing="rise_constraint")
        pprint(timing)
        # timing = get_timing(result, library="MC", cell="cell_name", port="A[1]", timing="rise_constraint")
        # pprint(timing)


    if 0:
        # list_text = "(a=b,b,c,(d, (e)))"
        # list_text = "(x,y) = (a=b,b,c,(d, (e)))"
        # list_text = "((e))"
        # list_text = "(e)"
        # list_text = "(a=e)"
        list_text = "(a,b)=(c,d)"
        # list_text = "(a,b)"
        print(list_text)
        lexer = Lexer(list_text)

        print('\n开始语法分析...')
        parser = AdvancedParser(lexer)
        tree = parser.parser()

if __name__ == "__main__":
    main()

    # text = """
    # server:
    #     host: localhost
    #     port: 8080

    # database:
    #     type: MySQL
    #     host: 127.0.0.1
    #     port: 3306
    #     username: root
    #     password: password
    # """
    # import yaml
    # data = yaml.safe_load(text)
    # print(data)
    # print(data['server']['host'])

    # {
    #     "version": "version 1",
    #     "result": {
    #         "pages": 1314,
    #         ...
    #     }
    # }

    # def dict_display(self):
    # def key_datnum(self):
    # def argument_list(self):
    # def positional_item(self):
    # def atom(self):

# <name> (<argument>) {
#     <key> : <value>;
#     ...
#     <name> (<argument>) {
#         <key> : <value>;
#         ...
#     }
# }

# <name> (<argument>) { ... }
# <key> : <value>;


# 依次匹配 bus -> timing -> rise_constraint -> values
# for line in w_lib:
#     if match(line, bus) == A:
#         flag = 1
#         ...
#         if match(line, timing) == "":
#             flag = 2
#             ...
#             if match(line, rise_constraint) == "CONSTRAINT":
#                 flag = 3
#                 ...
#                 match(line, values)
#                 ...
#             ...
#         ...
#     ...