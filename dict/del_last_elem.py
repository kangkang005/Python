def del_last_elem(name, **kwargs):
    while kwargs:
        print(kwargs.popitem())

if __name__ == "__main__":
    del_last_elem(12, first=1, second=2, third=3, fourth=4)