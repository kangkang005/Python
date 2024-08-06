def error_handling_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error occurred: {e}")
    return wrapper

@error_handling_decorator
def multiply(x, y):
    return x * y

print(multiply(1, 1, 2))