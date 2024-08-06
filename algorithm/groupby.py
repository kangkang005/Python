from pprint import *

def groupby(data, keys):
    def dfs(data, keys, path=None, found_list=None):
        if path is None:
            path = {}
        if found_list is None:
            found_list = result

        if not keys:
            # print(path)
            if not found_list:
                # create new group
                result.append(path)
                return path
            # get found group
            return found_list[0]

        key = keys[0]
        path[key] = data[key]
        new_found_list = []
        for found in found_list:
            # advanced search second key based on previous found_list
            if found[key] == data[key]:
                new_found_list.append(found)
        return dfs(data, keys[1:], path, new_found_list)

    result = []
    for dic in data:
        dfs(dic, keys).setdefault("list", []).append(dic)
    return result

if __name__ == "__main__":
    users = [
        {"username": "zhangsan", "age": 18, "gender": "man"},
        {"username": "lisi", "age": 20, "gender": "man"},
        {"username": "wanger", "age": 23, "gender": "man"},
        {"username": "mazi", "age": 19, "gender": "man"},
        {"username": "zhaowu", "age": 18, "gender": "female"},
        {"username": "maliu", "age": 22, "gender": "man"},
        {"username": "guiqi", "age": 18, "gender": "man"}
    ]

    result = groupby(users, keys=["age", "gender"])
    # result = groupby(users, keys=["age"])
    pprint(result)