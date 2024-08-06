from functools import wraps
import datetime
def dec(log_file):
    def dec_print_info(func):
        @wraps(func)
        def print_info(a,b):
            with open (log_file,'a+') as f:
                hour=datetime.datetime.now().hour
                minute=datetime.datetime.now().minute
                second=datetime.datetime.now().second
                f.write('call time: {}h {}m {}s, parameter: {} and {}\n'.format(hour,minute,second,a,b))
            return func(a,b)
        return print_info
    return dec_print_info

@dec('./log.txt')
def myfunc(a,b):
    return a+b
myfunc(12,59)