# Yacc example

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from calclex import tokens

# Grammar                             Action
# --------------------------------    --------------------------------------------
# expression0 : expression1 + term    expression0.val = expression1.val + term.val
#             | expression1 - term    expression0.val = expression1.val - term.val
#             | term                  expression0.val = term.val

# term0       : term1 * factor        term0.val = term1.val * factor.val
#             | term1 / factor        term0.val = term1.val / factor.val
#             | factor                term0.val = factor.val

# factor      : NUMBER                factor.val = int(NUMBER.lexval)
#             | ( expression )        factor.val = expression.val

# 在这个例子中，每个语法规则被定义成一个 Python 的方法，方法的文档字符串描述了相应的上下文无关文法，
# 方法的语句实现了对应规则的语义行为。每个方法接受一个单独的 p 参数，p 是一个包含有当前匹配语法的
# 符号的序列，p [i] 与语法符号的对应关系如下：
def p_expression_plus(p):
    'expression : expression PLUS term'
    #   ^            ^        ^    ^
    #  p[0]         p[1]     p[2] p[3]
    p[0] = p[1] + p[3]
# 其中，p [i] 的值相当于词法分析模块中对 p.value 属性赋的值，对于非终结符的值，将在归约时由 p [0] 的赋值决定，
# 这里的值可以是任何类型，当然，大多数情况下只是 Python 的简单类型、元组或者类的实例。在这个例子中，我们依赖
# 这样一个事实：NUMBER 标记的值保存的是整型值，所有规则的行为都是得到这些整型值的算术运算结果，并传递结果。

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

# @将语法规则合并
#   如果语法规则类似的话，可以合并到一个方法中。例如，考虑前面例子中的两个规则：
"""
def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]

def p_term_div(p):
    'term : term DIVIDE factor'
    p[0] = p[1] / p[3]
"""

# 比起写两个方法，你可以像下面这样写在一个方法里面：
def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    if p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# 默认的分析方法是 LALR，使用 SLR 请像这样运行 yacc ()：yacc.yacc (method="SLR")
# 注意：LRLR 生成的分析表大约要比 SLR 的大两倍。解析的性能没有本质的区别，因为代码是一样的。
# 由于 LALR 能力稍强，所以更多的用于复杂的语法。
# Build the parser
parser = yacc.yacc()
# 不生成分析表：yacc.yacc (write_tables=0)。注意：如果禁用分析表生成，
# yacc () 将在每次运行的时候重新构建分析表（这里耗费的时候取决于语法文件的规模）
# parser = yacc.yacc(write_tables=0)

while True:
   try:
       s = input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)