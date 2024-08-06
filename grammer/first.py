def compute_first(grammar):
    first = {}

    def compute(symbol):
        if symbol not in first:
            first[symbol] = set()
            for production in grammar[symbol]:
                if not production:
                    first[symbol].add('')
                elif production[0] not in grammar:
                    # if first is terminal, add terminal to first set
                    first[symbol].add(production[0])
                else:
                    # if first is non-terminal
                    for symbol_prime in production:
                        # skip that left non-terminal equal to right non-terminal
                        if symbol_prime != symbol:
                            compute(symbol_prime)
                            first[symbol] |= first[symbol_prime]
                            if '' not in first[symbol_prime]:
                                break
                            else:
                                first[symbol] -= {''}
        return first[symbol]

    for symbol in grammar:
        compute(symbol)

    return first

# 示例 BNF 文法
grammar = {
    '<expr>': [['<term>', '+', '<expr>'], ['<term>']],
    '<term>': [['<factor>', '*', '<term>'], ['<factor>']],
    '<factor>': [['(', '<expr>', ')'], ['a'], ['b']]
}

# 文法表示方式：BNF范式
grammar = {
    "<start>": [["<expr>"]],
    "<expr>": [["<term>"], ["<expr_tail>"]],
    "<expr_tail>": [["+", "<term>", "<expr_tail>"], ["-", "<term>", "<expr_tail>", ""]],
    "<term>": [["<factor>"],["<term_tail>"]],
    "<term_tail>": [["*", "<factor>"", <term_tail>"], ["/", "<factor>", "<term_tail>", ""]],
    "<factor>": [["(", "<expr>", ")"], ["<id>"], ["<num>"]],
    "<id>": [["a"], ["b"], ["c"]],
    "<num>": [["0"], ["1"], ["2"], ["3"], ["4"], ["5"], ["6"], ["7"], ["8"], ["9"]],
}

# @RULE:
#   lower is non-terminal
#   upper and symbol is terminal
grammar = {
    # dict grammar
    'dict_display':     [['{', 'dict_content', '}']],
    'dict_content' :    [['key_datum'], ["dict_content"]],
    'key_datum':        [['ID', 'property']],
    'property' :        [[':', 'atom', ';'], ['(', 'argument_list', ')', 'argument_tail']],
    'argument_tail' :   [[';'], ['dict_display']],
    'argument_list':    [['positional_item', ',', 'argument_list'], ['positional_item']],
    'positional_item':  [['atom']],
    'atom' :            [["ID"], ["INTEGER"], ["STRING"], ["REAL_CONST"], ["expr"]],

    # expression grammar
    'expr':             [['term',  'add_op', 'expr'], ['term']],
    'term':             [['factor', 'mul_op', 'term'], ['factor']],
    'factor':           [['(', 'expr', ')'], ['unary']],
    'add_op' :          [["+"], ["-"]],
    'mul_op' :          [["*"], ["/"], ["//"]],
    'unary' :           [['add_op', "num"], ["num"]],
    'num':              [['INTEGER'], ["REAL_CONST"]],

    # symbol name
    '(' :               [["LPAREN"]],
    ')' :               [["RPAREN"]],
    '{' :               [["LBRACE"]],
    '}' :               [["RBRACE"]],
    '+' :               [["PLUS"]],
    '-' :               [["MINUS"]],
    '*' :               [["MUL"]],
    '/' :               [["INTEGER_DIV"]],
    '//' :              [["FLOAT_DIV"]],
    '.' :               [["DOT"]],
    ',' :               [["COMMA"]],
    ';' :               [["COLON"]],
}

first_set = compute_first(grammar)
for symbol, first in first_set.items():
    print(f'First({symbol}): {first}')