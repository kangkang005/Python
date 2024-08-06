def validate_decorator(func):
    def wrapper(x, y):
        if isinstance(x, int) and isinstance(y, int):
            return func(x, y)
        else:
            raise ValueError("Input must be integers")
    return wrapper

@validate_decorator
def multiply(x, y):
    return x * y

print(multiply(1, 2))
print(multiply(1, 2.0))