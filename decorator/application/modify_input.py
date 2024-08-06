def modify_args_decorator(func):
    def wrapper(*args, **kwargs):
        new_args = [arg * 2 for arg in args]
        return func(*new_args, **kwargs)
    return wrapper

@modify_args_decorator
def multiply(x, y):
    return x * y

print(multiply(1, 2))