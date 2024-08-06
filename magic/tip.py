import copy
class Symbol (object):
    def __init__ (self, name, terminal = False):
        self.name = name
        self.term = terminal

    # 判断是否相等
    # 根据传入参数的类型进行判断
    def __eq__ (self, symbol):
        if isinstance(symbol, str):
            return (self.name == symbol)
        elif symbol is None:
            return (self is None)
        elif not isinstance(symbol, Symbol):
            raise TypeError('Symbol cannot be compared to a %s'%type(symbol))
        return (self.name == symbol.name)

    def __ne__ (self, symbol):
        return (not (self == symbol))

    # 求哈希，有这个函数可以将 Symbol 放到容器里当 key
    def __hash__ (self):
        return hash(self.name)

    # 拷贝
    def __copy__ (self):
        print("__copy___")
        obj = Symbol(self.name, self.term)
        if hasattr(self, 'value'):
            obj.value = self.value
        if hasattr(self, 'token'):
            obj.token = self.token
        return obj

    # 深度拷贝
    def __deepcopy__ (self, memo):
        print("__deepcopy___")
        obj = Symbol(self.name, self.term)
        if hasattr(self, 'value'):
            obj.value = copy.deepcopy(self.value, memo)
        if hasattr(self, 'token'):
            obj.token = copy.deepcopy(self.token, memo)
        return obj

if __name__ == "__main__":
    symbol1 = Symbol("Dot", True)
    symbol1.value = ["."]
    symbol2 = Symbol("Colon", True)
    print(symbol1 == symbol2)   # Symbol
    # False
    print(symbol1 == "Dot")     # str
    # True
    print(symbol1 != "Dot")     # str
    # False

    symbol_set = set()
    symbol_set.add(symbol1)
    print(symbol2 in symbol_set)
    # False
    print(Symbol("Dot") in symbol_set)
    # True

    copy_symbol1 = copy.copy(symbol1)
    # __copy__
    deepcopy_symbol1 = copy.deepcopy(symbol1)
    # __deepcopy__
    symbol1.value.append(";")
    print(copy_symbol1.value)
    # ['.', ';']
    print(deepcopy_symbol1.value)
    # ['.']