# @web: https://github.com/executablebooks/markdown-it-py/blob/master/markdown_it/token.py#L134
from typing import MutableMapping, Any, Union, Callable, Optional, Generator
from collections import OrderedDict

class BinaryNode:
    def __init__(
        self,
        left  = None,
        right = None,
        value = None
    ):
        self.left = left
        self.right = right
        self.value = value

    # dict to class
    @classmethod
    def from_dict(
        cls,
        dct: Union[MutableMapping[str, Any], Any]
    ) -> 'BinaryNode':
        node = cls()
        if not isinstance(dct, dict):
            node.value = dct
            return node
        if "left" in dct:
            node.left = cls.from_dict(dct["left"])
        if "right" in dct:
            node.right = cls.from_dict(dct["right"])
        return node

    # class to dict
    def as_dict(
        self,
        *,
        filter      : Optional[Callable[[str, Any], bool]]     = None,
        dict_factory : Callable[..., MutableMapping[str, Any]] = dict,
    ) -> MutableMapping[str, Any]:
        print(type(self)())
        '''
        :param filter: A callable whose return code determines whether an
            attribute or element is included (``True``) or dropped (``False``).
            Is called with the (key, value) pair.
        :param dict_factory: A callable to produce dictionaries from.
            For example, to produce ordered dictionaries instead of normal Python
            dictionaries, pass in ``collections.OrderedDict``.
        '''
        mapping = dict_factory()
        if self.left is None and self.right is None:
            if filter:
                return filter(self.value)
            return self.value
        if not self.left is None:
            mapping["left"] = self.left.as_dict(
                filter       = filter,
                dict_factory = dict_factory,
            )
        if not self.right is None:
            mapping["right"] = self.right.as_dict(
                filter       = filter,
                dict_factory = dict_factory,
            )
        return mapping

    def add_left(self, **kwargs):
        # 创建了一个与当前对象相同类的新对象
        left = type(self)(**kwargs)
        self.left = left
        return left

    def add_right(self, **kwargs):
        right = type(self)(**kwargs)
        self.right = right
        return right

    def walk(
        self,
    ) -> Generator[Any, None, None]:
        if self.left is None and self.right is None:
            yield self.value
        if not self.left is None:
            yield from self.left.walk()
        if not self.right is None:
            yield from self.right.walk()

    def __iter__(self):
        return self.walk()

if __name__ == "__main__":
    node = {
        "left" : 1,
        "right" : {
            "left": {
                "right" : 100,
            },
            "right" : -2
        }
    }
    node = BinaryNode.from_dict(node)
    print(node.left.value)
    print(node.right.right.value)
    print(node.as_dict())
    print(node.as_dict(dict_factory=OrderedDict))
    print(node.as_dict(filter=lambda key: key > 0))
    for n in node:
        print(n)

    node = BinaryNode()
    left = node.add_left()
    lol = left.add_left(value=2)
    rol = left.add_right(value=10)
    right = node.add_right(value=100)
    print(node.as_dict())