class Count:
    def __init__(self, func):
        self.func      = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        self.num_calls += 1
        print(f'num of calls is: {self.num_calls}')
        return self.func(*args, **kwargs)

@Count
def test_decorator():
    print("hello world")

test_decorator()
test_decorator()