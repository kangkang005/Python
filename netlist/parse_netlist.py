import re, os, sys, json
import traceback
from copy           import deepcopy
from collections    import OrderedDict
from pprint         import *
from device         import *

# Token
INTEGER       = 'INTEGER'
REAL          = 'REAL'
INTEGER_CONST = 'INTEGER_CONST'
REAL_CONST    = 'REAL_CONST'
PLUS          = 'PLUS'
MINUS         = 'MINUS'
MUL           = 'MUL'
INTEGER_DIV   = 'INTEGER_DIV'
FLOAT_DIV     = 'FLOAT_DIV'
LPAREN        = 'LPAREN'
RPAREN        = 'RPAREN'
LBRACE        = 'LBRACE'
RBRACE        = 'RBRACE'
ID            = 'ID'
ASSIGN        = 'ASSIGN'
BEGIN         = 'BEGIN'
END           = 'END'
SEMI          = 'SEMI'
DOT           = 'DOT'
PROGRAM       = 'PROGRAM'
VAR           = 'VAR'
COLON         = 'COLON'
COMMA         = 'COMMA'
EOF           = 'EOF'
PROCEDURE     = 'PROCEDURE'
STRING        = 'STRING'
EQUAL         = 'EQUAL'
COMMENT       = 'COMMENT'
NEWLINE       = 'NEWLINE'

##############################################
#  Lexer                                     #
##############################################
class Token:
    def __init__(self, type, value):
        self.type  = type
        self.value = value

    def __str__(self):
        return 'Token({type},{value})'.format(type=self.type, value=self.value)

    def __repr__(self):
        return self.__str__()

RESERVED_KEYWORDS = {
    'PROGRAM': Token(PROGRAM, 'PROGRAM'),
    'PROCEDURE': Token(PROCEDURE, 'PROCEDURE'),
    'VAR': Token(VAR, 'VAR'),
    'DIV': Token(INTEGER_DIV, 'DIV'),
    'INTEGER': Token(INTEGER, 'INTEGER'),
    'REAL': Token(REAL, 'REAL'),
    'BEGIN': Token(BEGIN, 'BEGIN'),
    'END': Token(END, 'END'),
}

class Lexer():
    def __init__(self, text):
        self.text          = text
        self.position      = 0
        self.current_char  = self.text[self.position]
        self.mark_stack    = []
        self.token_history = []

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

    def error(self):
        raise Exception('Warning: error input!')

    def advance(self):
        self.position += 1
        if self.position >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.position]
        return self.current_char

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char == " ":
            self.advance()

    # comment ::= "*" <any char> "\n"
    def skip_comment(self):
        comment = ""
        while not self.current_char == '\n':
            comment += self.current_char
            self.advance()
        # print(comment)
        while self.current_char == '\n':
            self.advance()

    # LL(k), LL(1) is that looks next one char, LL(k) is that looks next k chars
    # peek not consume any char
    def peek(self, k = 1):
        pos = self.position + k
        if pos >= len(self.text):
            return None
        else:
            return self.text[pos]

    def _id(self):
        result = ''
        while self.current_char is not None and \
            not self.current_char in ["=", "(", ")"] and \
            not self.current_char.isspace():
            result += self.current_char
            self.advance()
        token = RESERVED_KEYWORDS.get(result.upper(), Token('ID', result))
        return token

    def number(self):
        result = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):  # 如果当前字符不是None值并且当前字符是数字
            result += self.current_char
            self.advance()
        if ('.' in result):
            return Token(REAL_CONST,float(result))
        else:
            return Token(INTEGER_CONST,int(result))

    # @web: https://www.cnblogs.com/yubo-guan/p/18021690
    # <floating-point-number> ::= <digit-sequence> ['.' <digit-sequence>] [<exponent>]
    # <exponent>              ::= 'e' ['+' | '-'] <digit-sequence>
    # <digit-sequence>        ::= <digit> | <digit-sequence> <digit>
    # <digit>                 ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
    def number(self):
        result = ""
        result += self.digit_sequence()
        if self.current_char is not None and self.current_char == ".":
            result += self.current_char
            self.advance()
            result += self.digit_sequence()
        if self.current_char is not None and self.current_char.lower() == "e":
            result += self.current_char
            self.advance()
            if self.current_char is not None and self.current_char in ["-", "+"]:
                result += self.current_char
                self.advance()
            result += self.digit_sequence()
        # spice number
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        if result[-1].isalpha():
            return Token(STRING,result)
        elif ('e' in result):
            return Token(REAL_CONST,float(result))
        elif ('.' in result):
            return Token(REAL_CONST,float(result))
        else:
            return Token(INTEGER_CONST,int(result))

    def digit_sequence(self):
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
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

    # when need_history=False, not store history
    def get_next_token(self, need_history=True):
        def history_or_not(token, need_history):
            if need_history:
                self.token_history.append(token)

        while self.current_char is not None:
            if self.current_char == "\n":
                self.advance()
                while self.current_char is not None and self.current_char == "\n": # skip continuous whitespace line
                    self.advance()
                while self.current_char is not None and self.current_char == "*":    # skip NEWLINE MUL xxxx NEWLINE comment
                    self.advance()
                    self.skip_comment()
                if self.current_char is not None and self.current_char == "+":    # skip NEWLINE PLUS continuous line
                    self.advance()
                    continue
                    # return self.get_next_token(need_history)
                token = Token(NEWLINE, 'newline')
                history_or_not(token, need_history)
                return token
            # if self.current_char.isspace():
            if self.current_char == " ":
                self.skip_whitespace()
                continue
            if (not self.token_history or self.token_history[-1].type == NEWLINE) and self.current_char == '*':
                # consume start of comment * and previous token is newline or null
                self.advance()
                self.skip_comment()
                continue
            if self.current_char.isdigit():
                token = self.number()
                history_or_not(token, need_history)
                # print(token)
                return token
            if self.current_char == '+':
                self.advance()
                token = Token(PLUS, '+')
                history_or_not(token, need_history)
                return token
            if self.current_char == '-':
                self.advance()
                token = Token(MINUS, '-')
                history_or_not(token, need_history)
                return token
            if self.current_char == '*':
                self.advance()
                token = Token(MUL, '*')
                history_or_not(token, need_history)
                return token
            if self.current_char == '/':
                self.advance()
                token = Token(FLOAT_DIV, '/')
                history_or_not(token, need_history)
                return token
            if self.current_char == '(':
                self.advance()
                token = Token(LPAREN, '(')
                history_or_not(token, need_history)
                return token
            if self.current_char == ')':
                self.advance()
                token = Token(RPAREN, ')')
                history_or_not(token, need_history)
                return token
            if self.current_char == '{':
                self.advance()
                token = Token(LBRACE, '{')
                history_or_not(token, need_history)
                return token
            if self.current_char == '}':
                self.advance()
                token = Token(RBRACE, '}')
                history_or_not(token, need_history)
                return token
            if self.current_char.isalpha():
                token = self._id()
                # print(token)
                history_or_not(token, need_history)
                return token
            if self.current_char == ';':
                self.advance()
                token = Token(SEMI, ';')
                history_or_not(token, need_history)
                return token
            if self.current_char == '.':
                self.advance()
                token = Token(DOT, '.')
                history_or_not(token, need_history)
                return token
            if self.current_char == ':':
                self.advance()
                token = Token(COLON, ':')
                history_or_not(token, need_history)
                return token
            if self.current_char == ',':
                self.advance()
                token = Token(COMMA, ',')
                history_or_not(token, need_history)
                return token
            if self.current_char == '\"':
                self.advance()
                token = self.long_string()
                history_or_not(token, need_history)
                # print(token)
                return token
            if self.current_char == '\'':
                self.advance()
                token = self.short_string()
                history_or_not(token, need_history)
                # print(token)
                return token
            if self.current_char == '\\':
                self.advance()
                continue
            if self.current_char == '=':
                self.advance()
                token = Token(EQUAL, '=')
                history_or_not(token, need_history)
                return token
            self.error()
        if self.token_history[-1].type != NEWLINE:
            token = Token(NEWLINE, 'newline')
            history_or_not(token, need_history)
            return token
        token = Token(EOF, None)
        history_or_not(token, need_history)
        # print(self.token_history)
        return token

    def analyse(self):
        self.tokens = []
        while self.current_char is not None:
            token = self.get_next_token()
            self.tokens.append(token)
            print(token)
        return self.tokens

##############################################
#  Parser                                    #
##############################################
class AST(object):
    pass

################ Netlist #####################
class NetlistBlock(AST):
    def __init__(self, statements):
        self.statements = statements

class DotStatement(AST):
    def __init__(self):
        pass

class Temperature(AST):
    def __init__(self, keyword, temperatures):
        self.keyword      = keyword
        self.temperatures = temperatures

class Option(AST):
    def __init__(self, keyword, option):
        self.keyword = keyword
        self.option  = option

class Param(AST):
    def __init__(self, keyword, param):
        self.keyword = keyword
        self.param   = param

class Global(AST):
    def __init__(self, keyword, nodes):
        self.keyword = keyword
        self.nodes   = nodes

class Lib(AST):
    def __init__(self, keyword, path, entry_name=None):
        self.keyword    = keyword
        self.path       = path
        self.entry_name = entry_name

class Subckt_AST(AST):
    def __init__(self, keyword, name, ports, property, devices, netlist=None):
        self.keyword  = keyword
        self.name     = name
        self.ports    = ports
        self.property = property
        self.devices  = devices
        self.netlist  = netlist

class Model_AST(AST):
    def __init__(self, keyword, name, type, property):
        self.keyword  = keyword
        self.name     = name
        self.type     = type
        self.property = property

class InstSubckt(AST):
    def __init__(self, name, terminals, symbol, property):
        self.name      = name
        self.terminals = terminals
        self.property  = property
        self.symbol    = symbol

# mxxx d g s b
class Mosfet(InstSubckt):
    pass

# two terminals device
class Device2(AST):
    def __init__(self, name, terminals, symbol, property):
        self.name      = name
        self.terminals = terminals
        self.property  = property
        self.symbol    = symbol

class Resistor(Device2):
    pass

class Capacitor(Device2):
    pass

class Expression(AST):
    def __init__(self, elements):
        self.elements = elements

#############################################
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
            return self.current_token
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
                last_token = self.lexer.get_next_token(need_history=False)
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

    # <expr_str> = <factor_str> ([-+*/] <factor_str>)*
    # <factor_str> = (<expr_str>) | num | id
    def expr_str(self):
        nodes = []
        nodes.append(self.factor_str())
        while (self.current_token.type in (PLUS,MINUS,MUL,INTEGER_DIV,FLOAT_DIV)):
            nodes.append(self.current_token.value)
            self.eat(self.current_token.type)
            nodes.append(self.factor_str())
        return Expression(nodes)

    def factor_str(self):
        nodes = []
        token = self.current_token  # 获取记号
        if (token.type in (PLUS,MINUS)):
            nodes.append(token.value)
            self.eat(token.type)
            nodes.append(self.factor_str())
            return Expression(nodes)
        if (token.type in (INTEGER_CONST,REAL_CONST)):   # 整数
            self.eat(token.type)
            return Num(token)  # 返回数字节点对象
        elif (token.type == LPAREN):  # 左括号
            nodes.append(self.current_token.value)
            self.eat(LPAREN)
            nodes.append(self.expr_str())
            nodes.append(self.current_token.value)
            self.eat(RPAREN)                # 右括号
            return Expression(nodes)
        else:  # 新增变量因子
            node = self.variable()  # 获取变量节点
            return node  # 返回变量节点

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

class NetlistParser(Parser):
    def parser(self):
        node = self.stat()  # 获取程序所有节点
        if self.current_token.type != EOF:  # 如果当前不是文件末端记号
            self.error()  # 抛出异常
        return node  # 返回程序节点

    def stat(self):
        statements = []
        # while self.current_token.type in [MUL, DOT, ID]:
        while self.current_token.type in [MUL, DOT, ID]:
            if self.current_token.type == DOT:
                statements.append(self.dot_stat())
            elif self.current_token.type == ID:
                statements.append(self.device_stat())
            # elif self.current_token.type == MUL:
            #     self.comment()
        return NetlistBlock(statements=statements)

    def comment(self):
        self.eat(MUL)
        node = None
        comments = []
        while self.current_token.type != NEWLINE:
            comments.append(self.current_token.value)
            self.eat(self.current_token.type)
        self.eat(NEWLINE)
        node = Comment(comments)
        return node

    def dot_stat(self):
        self.eat(DOT)
        token_value = self.current_token.value.lower()
        if token_value in "title":
            return self.title_stat()
        elif token_value in "library":
            return self.lib_stat()
        elif token_value in "options":
            return self.option_stat()
        elif token_value in "global":
            return self.global_stat()
        elif token_value in "temperature":
            return self.temperature_stat()
        elif token_value in "param":
            return self.parameter_stat()
        elif token_value in "subckt":
            return self.subckt_stat()
        elif token_value in "model":
            return self.model_stat()
        return self.undef_dot_statement()

    def title_stat(self):
        while self.current_token.type != NEWLINE:
            self.eat(self.current_token.type)
        self.eat(NEWLINE)
        return DotStatement()

    def lib_stat(self):
        keyword = self.current_token.value
        self.eat(ID)
        path = self.current_token.value
        self.eat(STRING)
        node = None
        if self.current_token.type == ID:
            node = Lib(
                keyword    = keyword,
                path       = path,
                entry_name = self.current_token.value)
            self.eat(ID)
        else:
            node = Lib(
                keyword = keyword,
                path    = path)
        self.eat(NEWLINE)
        return node

    def option_stat(self):
        keyword = self.current_token
        self.eat(ID)
        option = OrderedDict()
        while self.current_token.type != NEWLINE:
            name = self.current_token.value
            self.eat(ID)
            if self.current_token.type == EQUAL:
                self.eat(EQUAL)
                value = self.current_token.value
                self.eat(self.current_token.type)
                option[name] = value
            else:
                option[name] = None
        self.eat(NEWLINE)
        return Option(keyword=keyword, option=option)

    def global_stat(self):
        keyword = self.current_token.value
        self.eat(ID)
        nodes = []
        while self.current_token.type != NEWLINE:
            nodes.append(self.current_token.value)
            self.eat(ID)
        self.eat(NEWLINE)
        return Global(keyword=keyword, nodes=nodes)

    def temperature_stat(self):
        keyword = self.current_token.value
        self.eat(ID)
        temperatures = []
        while self.current_token.type != NEWLINE:
            temperatures.append(self.current_token.value)
            self.eat(self.current_token.type)
        self.eat(NEWLINE)
        return Temperature(keyword=keyword, temperatures=temperatures)

    def undef_dot_statement(self):
        while self.current_token.type != NEWLINE:
            self.eat(self.current_token.type)
        self.eat(NEWLINE)
        return DotStatement()

    def parameter_stat(self):
        keyword = self.current_token.value
        self.eat(ID)
        param = OrderedDict()
        while self.current_token.type != NEWLINE:
            name = self.current_token.value
            self.eat(ID)
            self.eat(EQUAL)
            value = self.current_token.value
            self.eat(self.current_token.type)
            param[name] = value
        self.eat(NEWLINE)
        return Param(keyword=keyword, param=param)

    def model_stat(self):
        keyword = self.current_token.value
        self.eat(ID)
        name = self.current_token.value
        self.eat(ID)
        type = self.current_token.value
        self.eat(ID)
        property = []
        while self.current_token.type == ID:
            property.append(self.current_token.value)
            self.eat(ID)
            self.eat(EQUAL)
            property.append(self.atom())
        self.eat(NEWLINE)
        node = Model_AST(
            keyword  = keyword,
            name     = name,
            type     = type,
            property = property,
            )
        return node

    def subckt_stat(self):
        keyword = self.current_token.value
        self.eat(ID)
        name = self.current_token.value
        self.eat(ID)
        ports = []
        while self.current_token.type == ID and \
            (self.detect(1).type != EQUAL and self.detect(1).type != NEWLINE):
            ports.append(self.current_token.value)
            self.eat(ID)
        property = []
        while self.current_token.type == ID:
            property.append(self.current_token.value)
            self.eat(ID)
            self.eat(EQUAL)
            property.append(self.atom())
        self.eat(NEWLINE)   # parse .subckt line finish

        devices   = []
        statement = []
        while self.current_token.type in [DOT, ID]:
            if self.current_token.type == DOT and self.detect(1) and self.detect(1).value.lower() in ["end", "ends"]:
                break
            elif self.current_token.type == DOT:
                statement.append(self.dot_stat())
            elif self.current_token.type == ID:
                devices += self.device_stat()
        node = Subckt_AST(
            keyword  = keyword,
            name     = name,
            ports    = ports,
            property = property,
            devices  = devices,
            netlist  = NetlistBlock(statements=statement) if statement else None,
            )
        # .ends
        self.eat(DOT)
        self.eat(ID)
        if self.current_token.type == NEWLINE:
            self.eat(NEWLINE)
        return node

    def device_stat(self):
        devices = []
        while True:
            keyword = self.current_token
            if keyword.type == EOF:
                break
            elif keyword.value.lower()[0] == "x":
                node = self.inst_subckt_stat()
                devices.append(node)
            elif keyword.value.lower()[0] == "r":
                node = self.resistor_stat()
                devices.append(node)
            elif keyword.value.lower()[0] == "m":
                node = self.mosfet_stat()
                devices.append(node)
            else: # keyword.type == DOT
                break
        return devices

    def inst_subckt_stat(self):
        name = self.current_token.value
        self.eat(ID)
        terminals = []
        while self.current_token.type == ID \
            and ((self.detect(1) and self.detect(1).type in [ID, NEWLINE, FLOAT_DIV]) or not self.detect(1)):
            terminals.append(self.current_token.value)
            self.eat(ID)
            if self.current_token.type == FLOAT_DIV:
                self.eat(FLOAT_DIV)
        symbol = terminals.pop(-1)
        property = []
        while self.current_token.type == ID:
            property.append(self.current_token.value)
            self.eat(ID)
            self.eat(EQUAL)
            property.append(self.atom())
        self.eat(NEWLINE)
        return InstSubckt(
            name      = name,
            terminals = terminals,
            symbol    = symbol,
            property  = property,
        )

    def resistor_stat(self):
        name = self.current_token.value
        self.eat(ID)
        terminals = []
        terminals.append(self.current_token.value)
        self.eat(self.current_token.type)
        terminals.append(self.current_token.value)
        self.eat(self.current_token.type)
        symbol = None
        if self.current_token.type == ID:
            symbol = self.current_token.value
            self.eat(ID)
        r_value = None
        if self.current_token.type in self.atom_first_set():
            r_value = self.atom()
        elif self.current_token.type == ID and self.current_token.value.lower() == "r":
            self.eat(ID)
            self.eat(EQUAL)
            r_value = self.atom()
        property = []
        property.append("R")
        property.append(r_value)
        while self.current_token.type == ID:
            property.append(self.current_token.value)
            self.eat(ID)
            self.eat(EQUAL)
            property.append(self.atom())
        self.eat(NEWLINE)
        return Resistor(
            name      = name,
            terminals = terminals,
            symbol    = symbol,
            property  = property,
        )

    def mosfet_stat(self):
        name = self.current_token.value
        self.eat(ID)
        terminals = []
        i = 0
        while i < 5:
            terminals.append(self.current_token.value)
            self.eat(ID)
            i += 1
        symbol = terminals.pop(-1)
        property = []
        while self.current_token.type == ID:
            property.append(self.current_token.value)
            self.eat(ID)
            self.eat(EQUAL)
            property.append(self.atom())
        self.eat(NEWLINE)
        return Mosfet(
            name      = name,
            terminals = terminals,
            symbol    = symbol,
            property  = property,
        )

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
            # node = self.expr()
            node = self.expr_str()
        node = Atom(node)
        return node

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

class SubcktTable:
    def __init__(self):
        self._symbols = OrderedDict()  # 存储符号的有序字典
        self._init_builtins()  # 初始化内置类型

    def _init_builtins(self):  # 定义初始化内置类型的方法
        self.insert(BuiltinTypeSymbol('SUBCKT'))  # 通过insert()方法存入内置类型符号

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

class NetlistSemanticAnalyzer(NodeVisitor):  # 添加语义分析器
    def __init__(self):
        self.subckt_table = SubcktTable()

    def visit_DotStatement(self, node):
        pass

    def visit_Lib(self, node):
        pass

    def visit_InstSubckt(self, node):
        pass

    def visit_DotStatement(self, node):
        pass

    def visit_Global(self, node):
        pass

    def visit_Param(self, node):           # 添加访问字符串的方法
        pass

    def visit_NetlistBlock(self, node):
        for statement in node.statements:
            if not isinstance(statement, list):
                self.visit(statement)
            else:
                for device in statement:
                    self.visit(device)

    def visit_Subckt_AST(self, node):
        for device in node.devices:
            self.visit(device)

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

class NetlistInterpreter(NodeVisitor):
    def __init__(self, tree):  # 修改构造方法
        '''
        self.NETLIST = {
            "_global"     : set(),
            "_param"      : OrderedDict(),
            "_subckt"     : OrderedDict(),
            "_device"     : [],
            "_include"    : [],
            "_option"     : OrderedDict(),
            "_temperature": None,
        } # 创建全局存储字典
        '''
        self.tree    = tree  # 获取参数AST
        self.NETLIST = Netlist()

    def visit_Comment(self, node):
        return "\n".join(node.comments).strip()

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

    def visit_Expression(self, node):
        string = ""
        for element in node.elements:
            if isinstance(element, str):
                string += element
            else:
                string += str(self.visit(element))
        return string

    def visit_Num(self, node):  # 访问数字类型节点的方法
        return node.value

    def visit_String(self, node):
        return node.value

    def visit_Identifier(self, node):   # 添加访问ID的方法
        return node.name

    def visit_Variable(self, node):  # 访问变量节点
        var_name = node.name  # 获取变量名称
        return var_name

    def visit_Atom(self, node):     # 添加访问原子的方法
        return self.visit(node.atom)

    def visit_DotStatement(self, node):
        pass

    def visit_Lib(self, node):
        lib_data = {
            "path"      : node.path,
            "entry_name": node.entry_name,
            "netlist"   : parse_netlist(node.path)
        }
        # self.NETLIST["_include"].append(lib_data)
        return lib_data

    def visit_Temperature(self, node):
        # self.NETLIST["_temperature"] = node.temperatures
        return node.temperatures

    def visit_Option(self, node):
        # self.NETLIST["_option"].update(node.option)
        return node.option

    def visit_Param(self, node):
        # for key, value in node.param.items():
        #     self.NETLIST["_param"][key] = value
        return node.param

    def visit_Global(self, node):
        # for node_name in node.nodes:
        #     self.NETLIST["_global"].add(node_name)
        return node.nodes

    def visit_Model_AST(self, node):
        model = Model(node.name, node.type)
        while node.property:
            property_name  = node.property.pop(0)
            property_value = self.visit(node.property.pop(0))
            model.add_property(property_name, property_value)
        return model

    def visit_Subckt_AST(self, node):
        devices = []
        for device in node.devices:
            devices.append(self.visit(device))
        # self.NETLIST["_subckt"][node.name] = {
        #     "keyword" : node.keyword,
        #     "name"    : node.name,
        #     "ports"   : node.ports,
        #     "property": node.property,
        #     "devices" : devices,
        # }
        subckt = Subckt(node.name)
        for port in node.ports:
            subckt.add_port(port)
        for device in devices:
            subckt += device
        while node.property:
            property_name  = node.property.pop(0)
            property_value = self.visit(node.property.pop(0))
            subckt.add_property(property_name, property_value)
        if not node.netlist is None:
            subckt.set_netlist(self.visit(node.netlist))
        return subckt

    def visit_InstSubckt(self, node):           # 添加访问字符串的方法
        # return {
        #     "name"     : node.name,
        #     "terminals": node.terminals,
        #     "property" : node.property,
        #     "symbol"   : node.symbol,
        # }
        device = Device(node.name)
        device.set_symbol(node.symbol)
        for terminal in node.terminals:
            device.add_terminal(terminal)
        while node.property:
            property_name  = node.property.pop(0)
            property_value = self.visit(node.property.pop(0))
            device.add_property(property_name, property_value)
        return device

    def visit_Resistor(self, node):           # 添加访问字符串的方法
        device = Device(node.name)
        if node.symbol:
            device.set_symbol(node.symbol)
        for terminal in node.terminals:
            device.add_terminal(terminal)
        while node.property:
            property_name  = node.property.pop(0)
            property_value = self.visit(node.property.pop(0))
            device.add_property(property_name, property_value)
        return device

    def visit_Mosfet(self, node):           # 添加访问字符串的方法
        device = Device(node.name)
        device.set_symbol(node.symbol)
        for terminal in node.terminals:
            device.add_terminal(terminal)
        while node.property:
            property_name  = node.property.pop(0)
            property_value = self.visit(node.property.pop(0))
            device.add_property(property_name, property_value)
        return device

    def visit_NetlistBlock(self, node):
        netlist = Netlist()
        for statement in node.statements:
            if not isinstance(statement, list):
                if isinstance(statement, Subckt_AST):
                    netlist.append_subckt(self.visit(statement))
                elif isinstance(statement, Param):
                    netlist.append_param(self.visit(statement))
                elif isinstance(statement, Global):
                    netlist.append_global(self.visit(statement))
                elif isinstance(statement, Option):
                    netlist.append_option(self.visit(statement))
                elif isinstance(statement, Temperature):
                    netlist.set_temperature(self.visit(statement))
                elif isinstance(statement, Lib):
                    netlist.append_lib(self.visit(statement))
                elif isinstance(statement, Model_AST):
                    netlist.append_model(self.visit(statement))
            else:
                for device in statement:
                    netlist.append_device(self.visit(device))
        return netlist

    def interpret(self):  # 执行解释的方法
        tree = self.tree  # 获取AST
        if tree is None:  # 如果AST不存在
            return ''  # 返回空字符串
        return self.visit(tree)  # 否则访问AST


def parse_netlist(netlist_path):
    text = ""
    with open(netlist_path, "r") as r_netlist:
        text = r_netlist.read()
    lexer  = Lexer(text)
    parser = NetlistParser(lexer)
    tree   = parser.parser()
    interpreter = NetlistInterpreter(tree)
    netlist = interpreter.interpret()
    return netlist

def demo_netlist():
    text = ""
    with open("adder.cir", "r") as r_netlist:
        text = r_netlist.read()
    lexer  = Lexer(text)
    # tokens = lexer.analyse()
    # print(tokens)
    parser = NetlistParser(lexer)
    tree   = parser.parser()
    # print(tree)
    # semantic_analyzer  = NetlistSemanticAnalyzer()
    # semantic_analyzer.visit(tree)
    # print(semantic_analyzer.symbol_table)
    interpreter = NetlistInterpreter(tree)
    result = interpreter.interpret()
    # pprint(result)
    print(result)
    # for key, value in result.items():
    #     print(value)

    ### replace subckt
    # subckt = result.get_subckt("OR2")
    # subckt = deepcopy(subckt)
    # subckt.name = "OR"
    # result.replace_subckt(find_name="OR2", replace=subckt)
    # print(result)
    # print(result.get_subckt("OR2"))

    # print(result.find_top_subckt())
    # print(result.find_top_subckt1())
    # print(result.find_top_subckt2())

    # print(result.flatten_subckt(subckt_name="DOT", max_layer=2))
    # print(result.flatten_subckt())

    # print(result["AND2"])
    # print(result.get_subckt(name="AND2"))
    # print(result.get_device())
    # print(result.get_device(name="XINV"))

    # print(result.flatten_subckt())
    # print(result.trace_subckt(subckt_path="DOT.XOR10"))
    # print(result.trace_subckt(subckt_path="DOT.XOR1.XINV.xnmos"))
    # print(result.trace_subckt(subckt_path="DOT.XOR1"))
    # print(result.trace_subckt(subckt_path="DOT"))
    # print(result.trace_subckt(subckt_path="XDOT1.XOR1"))
    # print(result.trace_subckt(subckt_path="XDOT1"))
    # print(result.trace_subckt(subckt_path="xdot1"))
    # print(result.trace_subckt(subckt_path="xdot1.xor1"))
    # print(result.trace_subckt(subckt_path="dot.xor1"))
    # print(result.trace_subckt(subckt_path="dot.xor1", nocase=False))
    print(result.trace_subckt(subckt_path="mnmos", nocase=False))
    # subckt = result.get_subckt("OR2")
    subckt = result.get_subckt("INV2")
    print(subckt.get_net())
    # device = result.trace_subckt(subckt_path="XDOT1.XOR1.xpmos9")
    # print(device.get_neighbor())
    # print(subckt)
    # print(subckt.find_inverter())
    # print(subckt.highlight_net("VDD"))

    #     subckt.create_subckt("""
    # xnmos1 Y A GND GND lnfet l=length nfin=nfinn
    # xpmos1 Y A VDD VDD lpfet l=length nfin=nfinp
    # """.strip(), rename="INV3")

if __name__ == "__main__":
    demo_netlist()