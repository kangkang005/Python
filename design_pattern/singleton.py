class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta,cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def clear(cls):
         try:
            del SingletonMeta._instances[cls]
         except KeyError:
            pass

class SingletonClass(metaclass=SingletonMeta):
    pass

instance1 = SingletonClass()
instance2 = SingletonClass()
print(instance1)
print(instance2)