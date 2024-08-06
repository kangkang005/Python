import ply.yacc as yacc
from calclex import tokens

# @构造抽象语法树
#   yacc.py 没有构造抽像语法树的特殊方法。不过，你可以自己很简单的构造出来。
#   一个最为简单的构造方法是为每个语法规则创建元组或者字典，并传递它们。有很多中可行的方案，下面是一个例子：
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''

    p[0] = ('binary-expression',p[2],p[1],p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = ('group-expression',p[2])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ('number-expression',p[1])

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)