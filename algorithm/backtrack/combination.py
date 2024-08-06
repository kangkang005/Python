import copy
'''
# @web: https://zhuanlan.zhihu.com/p/93530380
回溯算法
for 选择 in 选择列表:
    # 做选择
    将该选择从选择列表移除
    路径.add(选择)
    backtrack(路径, 选择列表)
    # 撤销选择
    路径.remove(选择)
    将该选择再加入选择列表

void backtracking(参数) {
    if (终止条件) {
        存放结果;
        return;
    }
    for (选择：本层集合中元素（树中节点孩子的数量就是集合的大小）) {
        处理节点;
        backtracking(路径，选择列表); // 递归
        回溯，撤销处理结果
    }
}
'''
#  selection_list --cur_elem--> rest_list, path = [all cur_elem]
# [1, 2, 3] --1-->  [2, 3] --2--> [3] --3--> [],    path = [1, 2, 3]
# [1, 2, 3] --1-->  [2, 3] --3--> [2] --2--> [],    path = [1, 3, 2]
# [1, 2, 3] --2-->  [1, 3] --1--> [3] --3--> [],    path = [2, 1, 3]
# [1, 2, 3] --2-->  [1, 3] --3--> [1] --1--> [],    path = [2, 3, 1]
# [1, 2, 3] --3-->  [1, 2] --1--> [2] --2--> [],    path = [3, 1, 2]
# [1, 2, 3] --3-->  [1, 2] --2--> [2] --1--> [],    path = [3, 2, 1]
def combination(lst):
    def pop_list(lst, i):
        copy_lst = copy.deepcopy(lst)
        copy_lst.pop(i)
        return copy_lst

    result = []
    def backtrack(path = None, lst = lst):
        if not path:
            path = []
        if not lst:
            result.append(copy.deepcopy(path))
            return
        for i,elem in enumerate(lst):
            path.append(elem)
            backtrack(path, pop_list(lst, i))
            path.pop(-1)
    backtrack()
    return result

if __name__ == "__main__":
    lst = [1, 2, 3]
    print(combination(lst))