def repeat(count):
    def my_decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(count):
                print(f'counter: {i}')
            result = func(*args, **kwargs)
            return result
        return wrapper
    return my_decorator

@repeat(4)
def test_decorator(message):
    print(message)

test_decorator('hello world')