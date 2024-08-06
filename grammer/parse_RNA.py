G = "G"
C = "C"
A = "A"
U = "U"
EOF = "EOF"

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

    def cell(self):
        if self.current_char in ["A", "U", "G", "C"]:
            char = self.current_char
            self.advance()
            return Token(char, char)
        else:
            self.error()

    def get_next_token(self):
        while self.current_char is not None:  # 如果当前字符不是None值
            if self.current_char.isspace():  # 如果当前字符是空格
                self.skip_whitespace()  # 跳过所有空格
                continue
            if self.current_char.isalpha():  # 如果当前字符是字母
                return self.cell()
            self.error()  # 如果以上都不是，则抛出异常。
        return Token(EOF, None)  # 遍历结束返回结束标识创建的记号对象

class Parser:  #语法分析器
    def __init__(self, lexer):  # 定义构造方法获取用户输入的表达式
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token() # 语法分析器初始化

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

    # A-U, G-C, G-U
    # rna ::= G rna C rna | A rna U rna | None | EOF
    # rna ::= couple rna | None | EOF
    # couple ::= G rna C | C rna G | A rna U | U rna A | G rna U | U rna G
    # couple ::= G rna UC | C rna G | A rna U | U rna AG
    # UC :: = U | C
    # AG :: = A | G
    def rna(self):
        if self.current_token.type == G:
            self.eat(G)
            self.rna()
            self.eat(C)
            self.rna()
        elif self.current_token.type == A:
            self.eat(A)
            self.rna()
            self.eat(U)
            self.rna()
        elif self.current_token.type in [C, U]: # rna follow set
            pass
        elif self.current_token.type == EOF:
            pass
        else:
            self.error()

    def check(self, prev_token, current_token):
        if (prev_token.type == A and current_token.type == U) or \
            (prev_token.type == U and current_token.type == A) or \
            (prev_token.type == U and current_token.type == G) or \
            (prev_token.type == G and current_token.type == U) or \
            (prev_token.type == G and current_token.type == C) or \
            (prev_token.type == C and current_token.type == G):
            return True
        return False

    def matched(self):
        if self.stack and self.check(self.stack[-1], self.current_token):
            self.stack.pop(-1)
            return True
        return False

    def rna(self):
        # pre
        if self.matched():
            return
        else:
            self.stack.append(self.current_token)
        self._rna()
        # post
        if len(self.stack) > 1 and self.current_token.type == EOF:
            self.error()

    def _rna(self):
        if self.current_token.type in [A, U, C, G]:
            self.couple()
            self.rna()

    def couple(self):
        if self.current_token.type == G:
            self.eat(G)
            self.rna()
            self.uc()
        elif self.current_token.type == C:
            self.eat(C)
            self.rna()
            self.eat(G)
        elif self.current_token.type == A:
            self.eat(A)
            self.rna()
            self.eat(U)
        elif self.current_token.type == U:
            self.eat(U)
            self.rna()
            self.ag()

    def uc(self):
        if self.current_token.type == U:
            self.eat(U)
        elif self.current_token.type == C:
            self.eat(C)

    def ag(self):
        if self.current_token.type == A:
            self.eat(A)
        elif self.current_token.type == G:
            self.eat(G)

    def parser(self):
        self.stack = []
        node = self.rna()  # 获取程序所有节点
        if self.current_token.type != EOF:  # 如果当前不是文件末端记号
            self.error()  # 抛出异常
        return node  # 返回程序节点

def main():
    if 1 :
        # rna_txt = "GGAGCUCC"
        # rna_txt = "GGAGCUGCCCGC"
        rna_txt = "GGAUUGGCCCGC"
        # rna_txt = "GGAUUGGCCCGCG"
        print(rna_txt)
        lexer = Lexer(rna_txt)

        print('\n开始语法分析...')
        parser = Parser(lexer)
        tree = parser.parser()

if __name__ == "__main__":
    main()