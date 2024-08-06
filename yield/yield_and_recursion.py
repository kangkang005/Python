a = [1, 2, 3, [4, [5, 6, 7], 8], 9, 10, [11, 12, 13], 14]

"""
使用递归和循环虽然可以达到效果，但是需要把储存结果的列表作为参数不断递归的传入
"""
def spread_recursion(deep_list, result_list):
    for i in deep_list:
        if isinstance(i, list):
            spread_recursion(i, result_list)
        else:
            result_list.append(i)

if __name__ == "__main__":
    good_list = []
    spread_recursion(a, good_list)
    print(good_list)

"""
使用yield可以避免传入结果的列表
"""
def spread_yield(deep_list):
    for i in deep_list:
        if isinstance(i, list):
            # yield from是在python3.3之后才引入的
            yield from spread_yield(i)
        else:
            yield i

if __name__ == "__main__":
    result = [x for x in spread_yield(a)]
    print(result)