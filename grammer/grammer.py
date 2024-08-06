# run failed
# 文法表示方式：BNF范式
grammar = {
    "<start>":      ["<expr>"],
    "<expr>":       ["<term><expr_tail>"],
    "<expr_tail>":  ["+<term><expr_tail>", "-<term><expr_tail>", ""],
    "<term>":       ["<factor><term_tail>"],
    "<term_tail>":  ["*<factor><term_tail>", "/<factor><term_tail>", ""],
    "<factor>":     ["(<expr>)", "<id>", "<num>"],
    "<id>":         ["a", "b", "c"],
    "<num>":        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
}

def string2list(production):
    lst = []
    string = ""
    for char in production:
        string += char
        if char in ["+", "-", ">", ")", "*", "/"]:
            lst.append(string)
            string = ""
    if not lst:
        lst.append(production)
    return lst

# print(string2list("*<factor><term_tail>"))

# 计算First集
def calc_first(grammar):
    first = {}
    for symbol in grammar:
        first[symbol] = set()
    while True:
        updated = False
        for symbol in grammar:
            for production in grammar[symbol]:
                if production == "":
                    continue
                first_alpha = set()
                for alpha in string2list(production):
                    if alpha in first:
                        # print(alpha)
                        first_alpha |= first[alpha]
                    if alpha not in first:
                        first_alpha |= {alpha}
                        print(first_alpha)
                        break
                else:
                    if len(first_alpha - first[symbol]) > 0:
                        updated = True
                        first[symbol] |= first_alpha
        if not updated:
            break
    return first

# 计算Follow集
def calc_follow(grammar, first):
    follow = {}
    for symbol in grammar:
        follow[symbol] = set()
    follow["<start>"].add("$")
    while True:
        updated = False
        for symbol in grammar:
            for production in grammar[symbol]:
                for i, alpha in enumerate(production):
                    if alpha not in grammar:
                        continue
                    follow_alpha = set()
                    for beta in production[i + 1:]:
                        if beta in first:
                            follow_alpha |= first[beta] - {""}
                            if "" not in first[beta]:
                                break
                        else:
                            follow_alpha |= {beta}
                            break
                    else:
                        if len(follow_alpha - follow[alpha]) > 0:
                            updated = True
                            follow[alpha] |= follow_alpha
                    if "" in follow_alpha or i == len(production) - 1:
                        follow[symbol] |= follow[alpha]
                        if "" in follow_alpha:
                            follow[symbol] |= follow[symbol]
        if not updated:
            break
    return follow

# 测试
first = calc_first(grammar)
print("First set:")
for symbol in first:
    print(f"{symbol} -> {first[symbol]}")
follow = calc_follow(grammar, first)
print("Follow set:")
for symbol in follow:
    print(f"{symbol} -> {follow[symbol]}")