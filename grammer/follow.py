def compute_follow(grammar, start_symbol):
    follow = {non_terminal: set() for non_terminal in grammar.keys()}
    follow[start_symbol].add('$')

    def compute(symbol):
        for non_terminal, productions in grammar.items():
            for production in productions:
                if symbol in production:
                    symbol_index = production.index(symbol)
                    if symbol_index < len(production) - 1:
                        next_symbol = production[symbol_index + 1]
                        if next_symbol not in grammar:
                            follow[symbol] |= {next_symbol}
                        else:
                            first_set_next = compute_first(grammar, next_symbol)
                            follow[symbol] |= first_set_next - {''}
                            if '' in first_set_next:
                                follow[symbol] |= follow[non_terminal]
                                follow[symbol] -= {''}
                    else:
                        if non_terminal != symbol:
                            follow[symbol] |= follow[non_terminal]

    for non_terminal in grammar.keys():
        compute(non_terminal)

    return follow

def compute_first(grammar, symbol):
    first = set()

    def compute(symbol):
        if symbol not in first:
            first.add(symbol)
            for production in grammar[symbol]:
                if production[0] not in grammar:
                    first.add(production[0])
                elif production[0] != symbol:
                    compute(production[0])

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

# start_symbol = '<expr>'
# start_symbol = '<start>'
start_symbol = 'dict_display'
follow_set = compute_follow(grammar, start_symbol)
for symbol, follow in follow_set.items():
    print(f'Follow({symbol}): {follow}')