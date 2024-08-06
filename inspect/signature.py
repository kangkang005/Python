import inspect

def sample_function(name, age=25):
    pass

sig = inspect.signature(sample_function)
print(sig)  # (name, age=25)