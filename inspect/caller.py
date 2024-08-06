import inspect

def caller_info():
    frame = inspect.currentframe().f_back
    print(f"caller: {frame.f_code.co_filename} caller line: d{frame.f_lineno}")

def test():
    caller_info()  # caller info

test()