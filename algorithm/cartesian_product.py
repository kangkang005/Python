from copy import deepcopy
# @reference: https://stackoverflow.com/questions/533905/how-to-get-the-cartesian-product-of-multiple-lists

# cartesian product for list
def product(ar_list):
    if not ar_list:
        yield ()
    else:
        for a in ar_list[0]:
            for prod in product(ar_list[1:]):
                yield (a,)+prod

print(list(product([
    [1,2],
    [3,4],
    [5,6]
])))

# cartesian product for dictionary
def dict_product(hh):
    def _dict_product(hh):
        def pop_hh(hh, key):
            copy_hh = deepcopy(hh)
            copy_hh.pop(key)
            return copy_hh

        if not hh:
            yield {}
        else:
            key    = list(hh.keys())[0]
            values = hh[key]
            for value in values:
                rest = pop_hh(hh, key)
                for prod in _dict_product(rest):
                    yield {key: value, **prod}
    return list(_dict_product(hh))

print(dict_product({
    "test" : [1, 2, 3],
    "demo" : ["a", "b"],
    "dict" : ["10"],
}))