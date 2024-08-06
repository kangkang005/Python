# @web: https://blog.51cto.com/u_16175450/8492745
def del_first_elem(name, **kwargs):
    while kwargs:
        key = next(iter(kwargs))
        print(key, kwargs[key])
        del kwargs[key]

if __name__ == "__main__":
    del_first_elem(12, first=1, second=2, third=3, fourth=4)