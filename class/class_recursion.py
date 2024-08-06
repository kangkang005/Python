"""
在 Python 中，from __future__ import annotations 语句是用来引入 Python 3.7 中引入的类型注解功能的。
这个语句允许你在程序中声明变量或函数的类型，并由编译器或其他工具来检查代码的类型是否正确。
"""
from __future__ import annotations

import dataclasses as dc
from typing import Any, Literal
from collections.abc import Callable, MutableMapping
import textwrap

# @web: https://github.com/executablebooks/markdown-it-py/blob/master/markdown_it/token.py

"""
通过字典创建嵌套式对象
"""

@dc.dataclass
class Token:
    type: str
    """Type of the token (string, e.g. "paragraph_open")"""

    children: list[Token] | None = None
    attrs    : dict[str] | None  = None
    content  : str | None        = None

    @classmethod
    def from_dict(cls, dct: MutableMapping[str, Any]) -> Token:
        """Convert a dict to a Token."""
        token = cls(**dct)
        if token.children:
            token.children = [cls.from_dict(c) for c in token.children]  # type: ignore[arg-type]
        return token

    def pretty(
        self, *, indent: int = 2, show_text: bool = False, _current: int = 0
    ) -> str:
        """Create an XML style string of the tree."""
        prefix = " " * _current
        text = prefix + f"<{self.type}"
        if self.attrs:
            text += " " + " ".join(f"{k}={v!r}" for k, v in self.attrs.items())
        text += ">"
        if (
            show_text
            and self.type in ("text", "text_special")
            and self.content
        ):
            text += "\n" + textwrap.indent(self.content, prefix + " " * indent)
        for child in self.children:
            text += "\n" + child.pretty(
                indent=indent, show_text=show_text, _current=_current + indent
            )
        return text

if __name__ == "__main__":
    token_str = {
        "type": "paragraph_open",
        "children" : [
            {
                "type": "list_open",
                "children" : [
                    {
                        "type": "text",
                        "content":  "test",
                        "children": [],
                    },
                ]
            },
            {
                "type": "link",
                "attrs": {
                    "href": "https://nodeca.github.io/pica/demo/",
                },
                "children": [],
            },
            {
                "type": "list_close",
                "children": [],
            },
        ]
    }
    token = Token.from_dict(token_str)
    print(token)
    print(token.children[0])
    print(token.pretty(show_text=True))