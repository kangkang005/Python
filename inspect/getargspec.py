# @web: https://www.cnblogs.com/linxiyue/p/7989947.html
import inspect

# getargspec() get specific variable: args or kwargs
def attr_from_locals(locals_dict):
    self = locals_dict.pop('self')
    args = inspect.getfullargspec(self.__init__.__func__).args[1:]
    for k in args:
        setattr(self, k, locals_dict[k])
    # print(inspect.getfullargspec(self.__init__.__func__))
    # print(inspect.signature(self.__init__.__func__))
    keywords = inspect.getfullargspec(self.__init__.__func__).varkw
    if keywords:
        keywords_dict = locals_dict[keywords]
        for k in keywords_dict:
            setattr(self, k, keywords_dict[k])

class Foo(object):
    def __init__(self, name, **kwargs):
        attr_from_locals(locals())

f = Foo('bar', color='yellow', num=1)
print(f.__dict__)