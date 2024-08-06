import inspect
from pprint import *

def recurse(limit, keyword="default", * ,kwonly="must be named"):
    local_variable= "."*limit
    keyword = "change value of argument"
    frame = inspect.currentframe()
    print("line {} of {}".format(frame.f_lineno,frame.f_code.co_filename))
    pprint(frame.f_locals)

    print("\n")
    if limit <= 0:
        return
    recurse(limit-1)
    return local_variable

if __name__ == '__main__':
    recurse(2)