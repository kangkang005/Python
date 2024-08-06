# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex
from ply.lex import TOKEN

# @标记列表
#   词法分析器必须提供一个标记的列表，这个列表将所有可能的标记告诉分析器，用来执行各种验证，同时也提供给 yacc.py 作为终结符。
# List of token names.   This is always required
tokens = (
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'COMMENT',
)

# @标记的规则
#   每种标记用一个正则表达式规则来表示，每个规则需要以 "t_" 开头声明，表示该声明是对标记的规则定义。
#   对于简单的标记，可以定义成这样（在 Python 中使用 raw string 能比较方便的书写正则表达式）：
# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

# 这里，紧跟在 t_ 后面的单词，必须跟标记列表中的某个标记名称对应。如果需要执行动作的话，规则可以写成一个方法。
# 例如，下面的规则匹配数字字串，并且将匹配的字符串转化成 Python 的整型：
# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'  # 描述模式的正则表达式
    t.value = int(t.value)
    return t    # 最后必须返回t，如果不返回，这个token就会被丢弃掉
# 如果使用方法的话，正则表达式写成方法的文档字符串。方法总是需要接受一个 LexToken 实例的参数，
# 该实例有一个 t.type 的属性（字符串表示）来表示标记的类型名称，t.value 是标记值（匹配的实际的字符串），
# t.lineno 表示当前在源输入串中的作业行，t.lexpos 表示标记相对于输入串起始位置的偏移。
# 默认情况下，t.type 是以 t_开头的变量或方法的后面部分。方法可以在方法体里面修改这些属性。但是，如果这样做，应该返回结果 token，否则，标记将被丢弃。

# @丢弃标记
#   想丢弃像注释之类的标记，只要不返回 value 就行了，像这样：
def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded
# 为标记声明添加 "ignore_" 前缀同样可以达到目的：
t_ignore_COMMENT = r'\#.*'

# @行号和位置信息
#   默认情况下，lex.py 对行号一无所知。因为 lex.py 根本不知道何为 "行" 的概念（换行符本身也作为文本的一部分）。不过，可以通过写一个特殊的规则来记录行号：
# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
# 在这个规则中，当前 lexer 对象 t.lexer 的 lineno 属性被修改了，而且空行被简单的丢弃了，因为没有任何的返回。

# lex.py 也不自动做列跟踪。但是，位置信息被记录在了每个标记对象的 lexpos 属性中，这样，就有可能来计算列信息了。例如：每当遇到新行的时候就重置列值：
# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(input,token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column
# 通常，计算列的信息是为了指示上下文的错误位置，所以只在必要时有用。

# @忽略字符
#   t_ignore 规则比较特殊，是 lex.py 所保留用来忽略字符的，通常用来跳过空白或者不需要的字符。
#   虽然可以通过定义像 t_newline() 这样的规则来完成相同的事情，不过使用 t_ignore 能够提供较好的词法分析性能，因为相比普通的正则式，它被特殊化处理了。
# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# @错误处理
#   最后，在词法分析中遇到非法字符时，t_error() 用来处理这类错误。这种情况下，t.value 包含了余下还未被处理的输入字串，在之前的例子中，错误处理方法是这样的：
# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
# 这个例子中，我们只是简单的输出不合法的字符，并且通过调用 t.lexer.skip(1) 跳过一个字符。

# @TOKEN 装饰器
#   在一些应用中，你可能需要定义一系列辅助的记号来构建复杂的正则表达式，例如：
digit            = r'([0-9])'
nondigit         = r'([_A-Za-z])'
identifier       = r'(' + nondigit + r'(' + digit + r'|' + nondigit + r')*)'

# 在这个例子中，我们希望 ID 的规则引用上面的已有的变量。然而，使用文档字符串无法做到，为了解决这个问题，你可以使用 @TOKEN 装饰器：
@TOKEN(identifier)
def t_ID(t):
    ...

# @构建和使用 lexer
#   函数 lex.lex() 使用 Python 的反射机制读取调用上下文中的正则表达式，来创建 lexer。lexer 一旦创建好，有两个方法可以用来控制 lexer 对象：
#       lexer.input(data) 重置 lexer 和输入字串
#       lexer.token() 返回下一个 LexToken 类型的标记实例，如果进行到输入字串的尾部时将返回 None
#   推荐直接在 lex () 函数返回的 lexer 对象上调用上述接口，尽管也可以向下面这样用模块级别的 lex.input () 和 lex.token ()：
# Build the lexer
lexer = lex.lex()

if __name__ == "__main__":
    # Test it out
    data = '''
    # comment
    3 + 4 * 10
    + -20 *2
    '''

    # Give the lexer some input
    lexer.input(data)

    # Tokenize
    # while True:
    #     tok = lexer.token()
    #     if not tok: break      # No more input
    #     print(tok)

    # Lexers 也同时支持迭代，你可以把上面的循环写成这样：
    for tok in lexer:
        print(tok)
        print("type:", tok.type, "value:", tok.value, "lineno:", tok.lineno, "lexpos:", tok.lexpos)