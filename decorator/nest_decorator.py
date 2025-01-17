# order: top to bottom
import functools

def decorator1(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('decorator1')
        func(*args, **kwargs)
    return wrapper


def decorator2(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('decorator2')
        func(*args, **kwargs)
    return wrapper

def decorator3(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('decorator3')
        func(*args, **kwargs)
    return wrapper


@decorator1
@decorator2
@decorator3
def test_decorator(message):
    print(message)

test_decorator('hello world')