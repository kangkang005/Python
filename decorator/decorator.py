print("############ without decorator ##########")
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print('## before')
        func(*args, **kwargs)
        print('## after')
    return wrapper

def test_decorator(message):
    print(message)

decorator = my_decorator(test_decorator)
decorator('hello world')

print("############ with decorator ##########")
@my_decorator
def test_decorator(message):
    print(message)

test_decorator('i am decorator')
print(test_decorator.__name__)  # wrap meta info overwrite raw function info
help(test_decorator)

print("############ with functools ##########")
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('## before')
        func(*args, **kwargs)
        print('## after')
    return wrapper

@my_decorator
def test_decorator(message):
    print(message)

test_decorator('hello world')
print(test_decorator.__name__)  # reverse raw function info
help(test_decorator)