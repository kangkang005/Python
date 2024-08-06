class Count:
    def __init__(self, num):
        self.num_calls = num

    def __call__(self, func):
        print("begin decorator...")
        def wrap(*args, **kwargs):
            self.num_calls += 1
            print(f'num of calls is: {self.num_calls}')
            result = func(*args, **kwargs)
            return result
        return wrap

@Count(10)
def test_decorator():
    print("hello world")

test_decorator()
test_decorator()