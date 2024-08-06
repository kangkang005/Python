# @web: https://www.cnblogs.com/aaronhoo/p/14301750.html
import inspect

def get_attrs_of_module(module_name='temp'):
    module=__import__(module_name)
    # get class from imported module
    classes=[clsname for (clsname,fullname) in inspect.getmembers(module,inspect.isclass)]

    dic_cls_methods={}
    for clsname in classes:
        # get method of class
        methods = [
            method_name
            for (method_name,method) in inspect.getmembers(getattr(module,clsname),inspect.isfunction)
            # filter __init__ or magic method
            if not method_name.startswith("__")
        ]
        dic_cls_methods[clsname]=methods
    print(dic_cls_methods)

get_attrs_of_module("temp")