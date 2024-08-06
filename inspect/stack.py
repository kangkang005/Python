import inspect

def grandparent():
    parent()

def parent():
    child()

def child():
    for frame_record in inspect.stack():
        caller_frame = frame_record[0]
        info = inspect.getframeinfo(caller_frame)
        print(f"Function '{info.function}' called at line {info.lineno} of file {info.filename}")

# track call stack
grandparent()