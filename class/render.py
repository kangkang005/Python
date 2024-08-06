import inspect
from pprint import *

class Render():
    def __init__(self):
        self.rules = {
            # method name: executable instance method
            k: v
            for k, v in inspect.getmembers(self, predicate=inspect.ismethod)
            if not (k.startswith("render") or k.startswith("_"))
            # filter start with render and "_"
        }
        # self.rules["text"](*args, **kwargs)
        pprint(self.rules)

    def render(
        self, tokens
    ) -> str:
        result = ""

        for i, token in enumerate(tokens):
            if token["type"] == "inline":
                if token["children"]:
                    result += self.renderInline(token["children"])
            elif token["type"] in self.rules:
                result += self.rules[token["type"]](tokens, i)
            else:
                result += self.renderToken(tokens, i)

        return result

    def renderInline(
        self, tokens
    ) -> str:
        result = ""

        for i, token in enumerate(tokens):
            if token["type"] in self.rules:
                result += self.rules[token["type"]](tokens, i)
            else:
                result += self.renderToken(tokens, i)

        return result

    def renderToken(
        self,
        tokens,
        idx: int,
    ) -> str:
        result = ""
        needLf = False
        token = tokens[idx]

        # Tight list paragraphs
        if token["hidden"]:
            return ""

        # Insert a newline between hidden paragraph and subsequent opening
        # block-level tag.
        #
        # For example, here we should insert a newline before blockquote:
        #  - a
        #    >
        #
        if token["block"] and token["nesting"] != -1 and idx and tokens[idx - 1]["hidden"]:
            result += "\n"

        # Add token name, e.g. `<img`
        result += ("</" if token["nesting"] == -1 else "<") + token["tag"]

        # Encode attributes, e.g. `<img src="foo"`
        # result += self.renderAttrs(token)

        # Add a slash for self-closing tags, e.g. `<img src="foo" /`
        # if token["nesting"] == 0 and options["xhtmlOut"]:
        #     result += " /"

        # Check if we need to add a newline after this tag
        if token["block"]:
            needLf = True

            if token["nesting"] == 1 and (idx + 1 < len(tokens)):
                nextToken = tokens[idx + 1]

                if nextToken["type"] == "inline" or nextToken["hidden"]:
                    # Block-level tag containing an inline tag.
                    #
                    needLf = False

                elif nextToken["nesting"] == -1 and nextToken["tag"] == token["tag"]:
                    # Opening tag + closing tag of the same type. E.g. `<li></li>`.
                    #
                    needLf = False

        result += ">\n" if needLf else ">"

        return result

    def text(
        self, tokens, idx: int
    ) -> str:
        return tokens[idx]["content"]

    def code_inline(
        self, tokens, idx: int
    ) -> str:
        token = tokens[idx]
        return (
            "<code"
            # + self.renderAttrs(token)
            + ">"
            + tokens[idx]["content"]
            + "</code>"
        )

'''

---

# h1 Heading 8-)
## h2 Heading
Inline `code`
'''

node = [
    {
    "type": "hr",
    "tag": "hr",
    # "attrs": null,
    # "map": [
    #   10,
    #   11
    # ],
    "nesting": 0,
    "level": 0,
    "children": [],
    "content": "",
    "markup": "---",
    "info": "",
    # "meta": null,
    "block": True,
    "hidden": False
    },

    {
    "type": "heading_open",
    "tag": "h1",
    # "attrs": null,
    # "map": [
    #   12,
    #   13
    # ],
    "nesting": 1,
    # "level": 0,
    "children": False,
    "content": "",
    "markup": "#",
    "info": "",
    # "meta": null,
    "block": True,
    "hidden": False
  },
  {
    "type": "inline",
    "tag": "",
    # "attrs": null,
    # "map": [
    #   12,
    #   13
    # ],
    "nesting": 0,
    "level": 1,
    "children": [
      {
        "type": "text",
        "tag": "",
        # "attrs": null,
        # "map": null,
        "nesting": 0,
        "level": 0,
        "children": False,
        "content": "h1 Heading ",
        "markup": "",
        "info": "",
        # "meta": null,
        "block": False,
        "hidden": False
      },
      {
        "type": "emoji",
        "tag": "",
        # "attrs": null,
        # "map": null,
        "nesting": 0,
        "level": 0,
        "children": False,
        "content": "😎",
        "markup": "sunglasses",
        "info": "",
        # "meta": null,
        "block": False,
        "hidden": False
      }
    ],
    "content": "h1 Heading 8-)",
    "markup": "",
    "info": "",
    # "meta": null,
    "block": True,
    "hidden": False
  },
  {
    "type": "heading_close",
    "tag": "h1",
    # "attrs": null,
    # "map": null,
    "nesting": -1,
    "level": 0,
    "children": False,
    "content": "",
    "markup": "#",
    "info": "",
    # "meta": null,
    "block": True,
    "hidden": False
  },

  {
    "type": "heading_open",
    "tag": "h2",
    # "attrs": null,
    # "map": [
    #   13,
    #   14
    # ],
    "nesting": 1,
    "level": 0,
    "children": [],
    "content": "",
    "markup": "##",
    "info": "",
    # "meta": null,
    "block": True,
    "hidden": False
  },
  {
    "type": "inline",
    "tag": "",
    # "attrs": null,
    # "map": [
    #   13,
    #   14
    # ],
    "nesting": 0,
    "level": 1,
    "children": [
      {
        "type": "text",
        "tag": "",
        # "attrs": null,
        # "map": null,
        "nesting": 0,
        "level": 0,
        "children": [],
        "content": "h2 Heading",
        "markup": "",
        "info": "",
        # "meta": null,
        "block": False,
        "hidden": False
      }
    ],
    "content": "h2 Heading",
    "markup": "",
    "info": "",
    # "meta": null,
    "block": True,
    "hidden": False
  },
  {
    "type": "heading_close",
    "tag": "h2",
    # "attrs": null,
    # "map": null,
    "nesting": -1,
    "level": 0,
    "children": [],
    "content": "",
    "markup": "##",
    "info": "",
    # "meta": null,
    "block": True,
    "hidden": False
  },

  # code
  {
    "type": "paragraph_open",
    "tag": "p",
    # "attrs": null,
    # "map": [
    #   93,
    #   94
    # ],
    "nesting": 1,
    "level": 0,
    "children": [],
    "content": "",
    "markup": "",
    "info": "",
    # "meta": null,
    "block": True,
    "hidden": False
  },
  {
    "type": "inline",
    "tag": "",
    # "attrs": null,
    # "map": [
    #   93,
    #   94
    # ],
    "nesting": 0,
    "level": 1,
    "children": [
      {
        "type": "text",
        "tag": "",
        # "attrs": null,
        # "map": null,
        "nesting": 0,
        "level": 0,
        "children": [],
        "content": "Inline ",
        "markup": "",
        "info": "",
        # "meta": null,
        "block": False,
        "hidden": False
      },
      {
        "type": "code_inline",
        "tag": "code",
        # "attrs": null,
        # "map": null,
        "nesting": 0,
        "level": 0,
        "children": [],
        "content": "code",
        "markup": "`",
        "info": "",
        # "meta": null,
        "block": False,
        "hidden": False
      }
    ],
    "content": "Inline `code`",
    "markup": "",
    "info": "",
    # "meta": null,
    "block": True,
    "hidden": False
  },
  {
    "type": "paragraph_close",
    "tag": "p",
    # "attrs": null,
    # "map": null,
    "nesting": -1,
    "level": 0,
    "children": [],
    "content": "",
    "markup": "",
    "info": "",
    # "meta": null,
    "block": True,
    "hidden": False
  },
]

render = Render()
print(render.render(node))