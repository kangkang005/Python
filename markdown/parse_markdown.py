'''
markdown 无官方的 BNF
解析 markdown 解决思路是分四步:
1. 去除空行 / 注释 / 转义 /html 标签
2. 逐行解析，每行按照顺序依次用正则匹配，得到一颗基础 markdown 解析树
3. 联系上下文块优化一下，比如合并相同层级的引用块，代码块
4. markdown 解析树导出 html

词法分析
Markdown 的词法分析进行了简化，仅返回词素作为 token，因为：
1. Markdown 解析不需要类型信息，使用的标记符（比如 #、* 等）本身就是 token 类型和词素
2. 大部分场景下的 Markdown 解析不需要实现源码映射
Markdown 词法分析的具体实现是按行进行处理的，每次处理后词法分析器会记录当前读取位置，以便下次继续按行处理。

语法分析
CommonMark 规范中介绍了一种解析算法，分为两个阶段：
1. 构造所有块级节点，包括标题、块引用、代码块、分隔线、列表、段落等，还需要构造好链接引用定义映射表
2. 遍历每个块级节点，构造行级节点，包括文本、链接、强调、加粗等，链接的处理可能会需要查找步骤 1 中构造好的链接引用定义映射表

markdown
模式
markdown-it 提供了三种模式：commonmark、default、zero。分别对应最严格、GFM、最宽松的解析模式。

解析
markdown-it 的解析规则大体上分为块 (block) 和内联 (inline) 两种。具体可体现为
MarkdownIt.block 对应的是解析块规则的 ParserBlock， MarkdownIt.inline
对应的是解析内联规则的 ParserInline，MarkdownIt.renderer.render 和
MarkdownIt.renderer.renderInline 分别对应按照块规则和内联规则生成 HTML 代码。
'''

md_text = """
## 什么是 markdown
> Markdown 是一种轻量级的「标记语言」，它的优点很多，目前也被越来越多的写作爱好者...

## markdown 常用标签：
```
代码        (```)
引用        (>)
无序列表    ('*','-','+')
有序列表    ('1.','2.','3.')
标题        (#)
图片        (![]())
链接        ([]())
行内引用    (`)
粗体        (**)
斜体        (*)
表格
```
## markdown 入门1
1. [Markdown——入门指南](http://www.jianshu.com/p/1e402922ee32/)
2. [Markdown的基本语法](http://www.cnblogs.com/libaoquan/p/6812426.html)

### markdown 标签分类
- markdown 标签可以 **简单** 分为 2 大类：...
- 其中，*代码*、`引用`、无序列表、有序列表、标题这 5 类...
- 除了这 5 类标签外，图片，链接、行内引用、粗体、斜体这 5 类...
"""

"""
MarkdownAST.AbstractBlock
MarkdownAST.AbstractElement
MarkdownAST.AbstractInline
MarkdownAST.Admonition
MarkdownAST.Backslash
MarkdownAST.BlockQuote
MarkdownAST.Code
MarkdownAST.CodeBlock
MarkdownAST.DisplayMath
MarkdownAST.Document
MarkdownAST.Emph
MarkdownAST.FootnoteDefinition
MarkdownAST.FootnoteLink
MarkdownAST.HTMLBlock
MarkdownAST.HTMLInline
MarkdownAST.Heading
MarkdownAST.Image
MarkdownAST.InlineMath
MarkdownAST.Item
MarkdownAST.JuliaValue
MarkdownAST.LineBreak
MarkdownAST.Link
MarkdownAST.List
MarkdownAST.Paragraph
MarkdownAST.SoftBreak
MarkdownAST.Strong
MarkdownAST.Table
MarkdownAST.TableBody
MarkdownAST.TableCell
MarkdownAST.TableHeader
MarkdownAST.TableRow
MarkdownAST.Text
MarkdownAST.ThematicBreak
MarkdownAST.can_contain
MarkdownAST.isblock
MarkdownAST.iscontainer
MarkdownAST.isinline
MarkdownAST.tablerows
MarkdownAST.tablesize
"""

"""
0x09 is tab "\t"
0x0A is newline "\n"
0x20 is whitespace " "
"""
"""
Token 流
不像传统的 AST，我们使用更加底层的数据代表 - tokens。 不同之处一目了然：

* Tokens 是一个简单的序列（数组）。
* 打开的和关闭的标签是隔离的。
* 有特殊的 token 对象，比如 “内联容器 (inline container)”，它有嵌套的 tokens。
* 一系列内联的标签（粗体，斜体，文本等等）
参考 token class 以获得关于每个 token 内容的细节。

总之，一个 token 流是：

* 在顶层 - 是成对或单个 “块” tokens 的数组：
 ** 打开的 / 关闭的标题，列表，块引用，段落，...
 ** 代码，围栏块，水平规则，html 块，内联容器
* 每个内联 token 都有一个.children 属性，带有嵌套 token 流，用于内联内容：
 ** 打开的 / 关闭的 strong 强调，em 强调，链接，代码，...
 ** 文字，换行符
为什么不是 AST？因为我们的任务不需要它。我们遵循 KISS 原则。 如果你愿意的话 - 你可以在没有渲染器的情况下调用解析器并转换 tokens 流到 AST。
"""
class Token:
    def __init__(self, type, tag, nesting):
        #    Token#type -> String
        #       Type of the token (string, e.g. "paragraph_open")
        self.type     = type
        #    Token#tag -> String
        #       html tag name, e.g. "p"
        self.tag      = tag
        #    Token#attrs -> Array
        #       Html attributes. Format: `[ [ name1, value1 ], [ name2, value2 ] ]`
        # 对应 html 标签，如 <p>，<strong> 等。如果没有特别指定，renderer.render 将使用这个 tag 直接生成对应的 html 文本。
        self.attrs    = None
        #    Token#map -> Array
        #       Source map info. Format: `[ line_begin, line_end ]`
        # 表示 token 对应的 markdown 文本的位置，分别是开始行（包括），结束行（不包括）。
        self.map      = None
        #    Token#nesting -> Number
        #       Level change (number in {-1, 0, 1} set), where:
        #       -  `1` means the tag is opening
        #       -  `0` means the tag is self-closing
        #       - `-1` means the tag is closing
        self.nesting  = nesting
        #    Token#level -> Number
        #       nesting level, the same as `state.level`
        # 嵌套级别，对应 html 就很好理解。Html 标签有开有闭，开就对应 1，闭对应 - 1，中间就是 0.
        self.level    = 0
        #    Token#children -> Array
        #       An array of child nodes (inline and img tokens)
        self.children = None
        #    Token#content -> String
        #       In a case of self-closing tag (code, html, fence, etc.),
        #       it has contents of this tag.
        self.content  = ''
        #    Token#markup -> String
        #       '*' or '_' for emphasis, fence string for fence, etc.
        self.markup   = ''
        #    Token#info -> String
        #       Additional information:
        #           - Info string for "fence" tokens
        #           - The value "auto" for autolink "link_open" and "link_close" tokens
        #           - The string value of the item marker for ordered-list "list_item_open" tokens
        self.info     = ''
        #    Token#meta -> Object
        #       A place for plugins to store an arbitrary data
        self.meta     = None
        #    Token#block -> Boolean
        #       True for block-level tokens, false for inline tokens.
        #       Used in renderer to calculate line breaks
        self.block    = False
        #    Token#hidden -> Boolean
        #       If it's true, ignore this element when rendering. Used for tight lists
        #       to hide paragraphs.
        self.hidden   = False

    # Token.attrIndex(name) -> Number
    # Search attribute index by name.
    def attrIndex(self, name):
        if not self.attrs:
            return -1

        attrs = self.attrs

        i = 0
        length = len(attrs)
        while i < length:
            if attrs[i][0] == name:
                return i
        return -1

    # Token.attrPush(attrData)
    # Add `[ name, value ]` attribute to list. Init attrs if necessary
    def attrPush(self, attrData):
        if self.attrs:
            self.attrs.append(attrData)
        else:
            self.attrs = [attrData]

    # Token.attrSet(name, value)
    # Set `name` attribute to `value`. Override old value if exists.
    def attrSet(self, name, value):
        idx = self.attrIndex(name)
        attrData = [name, value]
        if idx < 0:
            self.attrPush(attrData)
        else:
            self.attrs[idx] = attrData

    # Token.attrGet(name)
    # Get the value of attribute `name`, or null if it does not exist.
    def attrGet(self, name):
        idx = self.attrIndex(name)
        value = None
        if idx >= 0:
            value = self.attrs[idx][1]
        return value

    # Token.attrJoin(name, value)
    # Join value to existing attribute via space. Or create new attribute if not
    # exists. Useful to operate with token classes.
    def attrJoin(self, name, value):
        idx = self.attrIndex(name)

        if idx < 0:
            self.attrPush([name, value])
        else:
            self.attrs[idx][1] = self.attrs[idx][1] + " " + value

"""
 * class Ruler
 *
 * Helper class, used by [[MarkdownIt#core]], [[MarkdownIt#block]] and
 * [[MarkdownIt#inline]] to manage sequences of functions (rules):
 *
 * - keep rules in defined order
 * - assign the name to each rule
 * - enable/disable rules
 * - add/replace rules
 * - allow assign rules to additional named chains (in the same)
 * - cacheing lists of active rules
 *
 * You will not need use this class directly until write plugins. For simple
 * rules control use [[MarkdownIt.disable]], [[MarkdownIt.enable]] and
 * [[MarkdownIt.use]].
"""
class Ruler:
    def __init__(self):
        # List of added rules. Each element is:
        # {
        #   name: XXX,
        #   enabled: Boolean,
        #   fn: Function(),
        #   alt: [ name2, name3 ]
        # }
        self.__rules__ = []

        # Cached rule chains.
        # First level - chain name, '' for default.
        # Second level - diginal anchor for fast filtering by charcodes.
        self.__cache__ = None

    # Helper methods, should not be used directly
    # Find rule index by name
    def __find__(self, name):
        i = 0
        while i < len(self.__rules__):
            if self.__rules__[i].name == name:
                return i
        return -1

    # Build rules lookup cache
    def __compile__(self):
        chains = ['']

        # collect unique names
        for rule in self.__rules__:
            if not rule.enabled:
                return
            for altName in rule.alt:
                if not altName in chains:
                    chains.append(altName)

        self.__cache__ = {}
        for chain in chains:
            self.__cache__[chain] = []
            for rule in self.__rules__:
                if not rule.enabled:
                    return
                if chain and not chain in rule.alt:
                    return
                self.__cache__[chain].append(rule.fn)

    """
    * Ruler.at(name, fn [, options])
    * - name (String): rule name to replace.
    * - fn (Function): new rule function.
    * - options (Object): new rule options (not mandatory).
    *
    * Replace rule by name with new function & options. Throws error if name not
    * found.
    *
    * ##### Options:
    *
    * - __alt__ - array with names of "alternate" chains.
    *
    * ##### Example
    *
    * Replace existing typographer replacement rule with new one:
    *
    * ```javascript
    * var md = require('markdown-it')();
    *
    * md.core.ruler.at('replacements', function replace(state) {
    *   //...
    * });
    * ```
    """
    def at(self, name, fn, options):
        index = self.__find__(name)
        opt   = options if options else {}

        if index == -1:
            raise Exception('Parser rule not found: ' + name)

        self.__rules__[index].fn = fn
        self.__rules__[index].alt = opt.alt if opt.alt else []
        self.__cache__ = None


class StateBlock():
    def __init__(self, src, md, env, tokens):
        # 保存了 normalize 之后的 markdown 全文
        self.src = src
        #   link to parser instance
        self.md  = md

        self.env = env

        # Internal state variables

        self.tokens = tokens

        # 每一行开始的 index（包括行首空格）
        self.bMarks = []  # line begin offsets for fast jumps
        # 每一行行尾 index（指向换行，最后一行可能没有换行符，那就指向最后一个字符）
        self.eMarks = []  # line end offsets for fast jumps
        # 每一行行首的空白符数量，tab 算一个，程序中位置跳转会用到
        self.tShift = []  # offsets of the first non-space characters (tabs not expanded)
        # 每一行行首的空白符数量，tab 展开，视位置算 1~4 个。分析 markdown 逻辑时需要用到
        self.sCount = []  # indents for each line (tabs expanded)

        # An amount of virtual spaces (tabs expanded) between beginning
        # of each line (bMarks) and real beginning of that line.
        #
        # It exists only as a hack because blockquotes override bMarks
        # losing information in the process.
        #
        # It's used only when expanding tabs, you can think about it as
        # an initial tab length, e.g. bsCount=21 applied to string `\t123`
        # means first tab should be expanded to 4-21%4 === 3 spaces.
        self.bsCount = []

        # block parser variables

        # required block content indent (for example, if we are
        # inside a list, it would be positioned after list marker)
        self.blkIndent  = 0
        self.line       = 0         # line index in src
        self.lineMax    = 0         # lines count
        self.tight      = False     # loose/tight mode for lists
        self.ddIndent   = -1        # indent of the current dd block (-1 if there isn't any)
        self.listIndent = -1        # indent of the current list block (-1 if there isn't any)

        # can be 'blockquote', 'list', 'root', 'paragraph' or 'reference'
        # used in lists to determine if they interrupt a paragraph
        self.parentType = 'root'

        self.level = 0

        # Create caches
        # Generate markers.
        s = self.src

        start = 0
        indent = 0
        offset = 0
        length = len(s)
        indent_found = False        # indent is at begin of line if indent_found = False
        pos = 0
        while pos < length:
            try:
                ch = s[pos]
                if not indent_found:
                    if ch in [" ", "\t"]:
                        indent += 1
                        if ch == "\t":
                            offset += 4 - offset % 4
                        else:
                            offset += 1
                        continue
                    else:
                        indent_found = True
                if ch == "\n" or pos == length - 1:
                    if ch != "\n":
                        pos += 1
                    self.bMarks.append(start)
                    self.eMarks.append(pos)
                    self.tShift.append(indent)
                    self.sCount.append(offset)
                    self.bsCount.append(0)

                    # skip newline and reset variable
                    indent_found = False
                    indent       = 0
                    offset       = 0
                    start        = pos + 1
            finally:
                pos += 1

        # Push fake entry to simplify cache bounds checks
        self.bMarks.append(len(s))
        self.eMarks.append(len(s))
        self.tShift.append(0)
        self.sCount.append(0)
        self.bsCount.append(0)

        self.lineMax = len(self.bMarks) - 1 # don't count last fake line

    # Push new token to "stream".
    def push(self, type, tag, nesting):
        token       = Token(type, tag, nesting)
        token.block = True

        if nesting < 0:
            # closing tag
            self.level -= 1
        token.level = self.level
        if nesting > 0:
            # opening tag
            self.level += 1

        self.tokens.append(token)
        return token

    # whitespace or indent or null line is regarded as empty
    # @param:
    #   line: line number
    def isEmpty(self, line):
        return self.bMarks[line] + self.tShift[line] >= self.eMarks[line]

    # skip continuous empty line
    def skipEmptyLines(self, _from):
        while _from < self.lineMax:
            if not self.isEmpty(_from):
                break
            _from += 1
        return _from

    # Skip continuous spaces from given position.
    def skipSpaces(self, pos):
        while pos < len(self.src):
            ch = self.src[pos]
            if not ch in [" ", "\t"]:
                break
        return pos

    # Skip spaces from given position in reverse.
    def skipSpacesBack(self, pos, _min):
        if pos <= _min:
            return pos

        while pos > _min:
            pos -= 1
            ch = self.src[pos]
            if not ch in[" ", "\t"]:
                return pos + 1
        return pos

    # Skip char codes from given position
    def skipChars(self, pos, code):
        while pos < len(self.src):
            ch = self.src[pos]
            if ch != code:
                break
        return pos

    # Skip char codes reverse from given position - 1
    def skipCharsBack(self, pos, code, _min):
        if pos <= _min:
            return pos
        while pos > _min:
            pos -= 1
            ch = self.src[pos]
            if ch != code:
                return pos + 1
        return pos

    # cut lines range from source.
    # @param:
    #   begin:      begin line number
    #   end:        end line number
    #   indent:     remove indent number
    #   keepLastLF: ?
    def getLines(self, begin, end, indent, keepLastLF):
        if begin >= end:
            return ""
        queue = [""] * (end-begin)

        i    = 0
        line = begin
        while line < end:
            lineIndent = 0
            lineStart  = self.bMarks[line]
            first      = lineStart
            last       = None

            if line + 1 < end or keepLastLF:
                # No need for bounds check because we have fake entry on tail.
                last = self.eMarks[line] + 1
            else:
                last = self.eMarks[line]

            while first < last and lineIndent < indent:
                ch = self.src[first]

                if ch in [" ", "\t"]:
                    if ch == "\t":
                        lineIndent += 4 - (lineIndent + self.bsCount[line]) % 4
                    else:
                        lineIndent += 1
                elif first - lineStart < self.tShift[line]:
                    # patched tShift masked characters to look like spaces (blockquotes, list markers)
                    lineIndent += 1
                else:
                    break
                first += 1
            if lineIndent > indent:
                # partially expanding tabs in code blocks, e.g '\t\tfoobar'
                # with indent=2 becomes '  \tfoobar'
                queue[i] = " " * (lineIndent - indent + 1) + self.src[first:last]
            else:
                queue[i] = self.src[first:last]
            line += 1
            i += 1
        return "".join(queue)

# @Heading
def heading(state, startLine, endLine, silent):
    pos  = state.bMarks[startLine] + state.tShift[startLine]
    _max = state.eMarks[startLine]

    # if it's indented more than 3 spaces, it should be a code block
    # such as: "     #" or "       #"
    if state.sCount[startLine] - state.blkIndent >= 4:
        return False

    ch = state.src[pos]

    if not ch == "#" or pos >= _max:
        return False

    # count heading level, # number is level number
    level = 1
    pos += 1
    ch = state.src[pos]
    while ch == "#" and pos < _max and level <= 6:
        level += 1
        pos += 1
        ch = state.src[pos]

    if level > 6 or (pos < _max and not ch in [" ", "\t"]):
        return False

    if silent:
        return True

    # Let's cut tails like '    ###  ' from the end of string

    _max = state.skipSpacesBack(_max, pos)
    tmp  = state.skipCharsBack(_max, "#", pos)
    if tmp > pos and state.src[tmp-1] in [" ", "\t"]:
        _max = tmp

    state.line = startLine + 1

    token_o        = state.push("heading_open", "h"+str(level), 1)
    token_o.markup = "########"[0:level]
    token_o.map    = [startLine, state.line]

    token_i          = state.push("inline", "", 0)
    token_i.content  = state.src[pos:_max].strip()
    token_i.map      = [startLine, state.line]
    token_i.children = []

    token_c        = state.push("heading_close", "h"+str(level), -1)
    token_c.markup = "########"[0:level]

    return True

# @Code
def code(state, startLine, endLine):
    if state.sCount[startLine] - state.blkIndent >= 4:
        return False

    nextLine = startLine + 1
    last     = nextLine

    while nextLine < endLine:
        if state.isEmpty(nextLine):
            nextLine += 1
            continue

        if state.sCount[nextLine] - state.blkIndent >= 4:
            nextLine += 1
            last = nextLine
            continue
        break

    state.line = last

    token          = state.push("code_block", "code", 0)
    token.content  = state.getLines(startLine, last, 4 + state.blkIndent, False) + "\n"
    token.map      = [startLine, state.line]

    return True

# @Paragraph
def paragraph(state, startLine, endLine):
    terminatorRules  = state.md.block.rule.getRules("paragraph")
    oldParentType    = state.parentType
    nextLine         = startLine + 1
    state.parentType = "paragraph"

    # jump line-by-line until empty one or EOF
    while nextLine < endLine and not state.isEmpty(nextLine):
        try:
            # this would be a code block normally, but after paragraph
            # it's considered a lazy continuation regardless of what's there
            if state.sCount[startLine] - state.blkIndent >= 4:
                continue

            # quirk for blockquotes, this line should already be checked by that rule
            if state.sCount[nextLine] < 0:
                continue

            # Some tags can terminate paragraph without empty line.
            terminate = False
            i = 0
            l = len(terminatorRules)
            while i < l:
                if terminatorRules[i](state, nextLine, endLine, True):
                    terminate = True
                    break
            if terminate:
                break
        finally:
            i += 1

    content = state.getLines(startLine, nextLine, state.blkIndent, False).strip()

    state.line = nextLine

    token_o        = state.push("paragraph_open", "p", 1)
    token_o.map    = [startLine, state.line]

    token_i          = state.push("inline", "", 0)
    token_i.content  = content
    token_i.map      = [startLine, state.line]
    token_i.children = []

    state.push("paragraph_close", "p", -1)
    state.parentType = oldParentType

    return True

# @Lists
# Search `[-+*][\n ]`, returns next pos after marker on success or -1 on fail.
def skipBulletListMarker(state, startLine):
    _max = state.eMarks[startLine]
    pos = state.bMarks[startLine] + state.tShift[startLine]

    marker = state.src[pos]
    pos += 1
    # Check bullet
    if not marker in ["*", "-", "+"]:
        return -1

    if pos < _max:
        ch = state.src[pos]
        if not ch in [" ", "\t"]:
            # " -test " - is not a list item
            return -1
    return pos

# Search `\d+[.)][\n ]`, returns next pos after marker on success or -1 on fail.
def skipOrderedListMarker(state, startLine):
    _max = state.eMarks[startLine]
    start = state.bMarks[startLine] + state.tShift[startLine]
    pos = start

    # List marker should have at least 2 chars (digit + dot)
    if pos + 1 >= _max:
        return -1

    ch = state.src[pos]
    pos += 1
    # Check bullet
    if ch not in "0123456789":
        return -1

    while True:
        # EOL -> fail
        if pos >= _max:
            return -1

        ch = state.src[pos]
        pos += 1

        if ch in "0123456789":
            # List marker should have no more than 9 digits
            # (prevents integer overflow in browsers)
            if pos - start >= 10:
                return -1
            continue

        if ch in [")", "."]:
            break

        return -1

    if pos < _max:
        ch = state.src[pos]
        if not ch in [" ", "\t"]:
            # " 1.test " - is not a list item
            return -1
    return pos

def markTightParagraphs(state, idx):
    level = state.level + 2

    i = idx + 2
    l = len(state.tokens) - 2
    while i < l:
        if state.tokens[i].level == level and \
            state.tokens[i].type == "paragraph_open":
            state.tokens[i+2].hidden = True
            state.tokens[i].hidden   = True
            i += 2

def list(state, startLine, endLine, silent):
    _max = None
    pos = None
    start = None
    token = None
    nextLine = startLine
    tight = True

    # if it's indented more than 3 spaces, it should be a code block
    if state.sCount[nextLine] - state.blkIndent >= 4:
        return False

    # Special case:
    #  - item 1
    #   - item 2
    #    - item 3
    #     - item 4
    #      - this one is a paragraph continuation
    if state.listIndent >= 0 and \
        state.sCount[nextLine] - state.listIndent >= 4 and \
        state.sCount[nextLine] < state.blkIndent:
        return False

    isTerminatingParagraph = False

    # limit conditions when list can interrupt a paragraph (validation mode only)
    if silent and state.parentType == "paragraph":
        # Next list item should still terminate previous list item;
        # This code can fail if plugins use blkIndent as well as lists,
        # but I hope the spec gets fixed long before that happens.
        if state.sCount[nextLine] >= state.blkIndent:
            isTerminatingParagraph = True

    # Detect list type and position after marker
    isOrdered = None
    markerValue = None
    posAfterMarker = skipOrderedListMarker(state, nextLine)
    if posAfterMarker >= 0:
        isOrdered = True
        start = state.bMarks[nextLine] + state.tShift[nextLine]
        markerValue = int(state.src[start, posAfterMarker-1])   # plus 1 is plus point(.)

        # If we're starting a new ordered list right after
        # a paragraph, it should start with 1.
        if isTerminatingParagraph and not markerValue == 1:
            return False
    else:
        posAfterMarker = skipBulletListMarker(state, nextLine)
        if posAfterMarker >= 0:
            isOrdered = False
        else:
            return False

    # If we're starting a new unordered list right after
    # a paragraph, first line should not be empty.
    if isTerminatingParagraph:
        if state.skipSpaces(posAfterMarker) >= state.eMarks[nextLine]:
            return False

    # For validation mode we can terminate immediately
    if silent:
        return True

    # We should terminate list on style change. Remember first one to compare.
    markerCharCode = state.src[posAfterMarker-1]

    # Start list
    listTokIdx = len(state.tokens)

    if isOrdered:
        token = state.push("ordered_list_open", "ol", 1)
        if not markerValue == 1:
            token.attrs = [["start", markerValue]]
    else:
        token = state.push("bullet_list_open", "ul", 1)

    listLines = [nextLine, 0]
    token.map = listLines
    token.markup = str(markerCharCode)

    # Iterate list items
    prevEmptyEnd    = False
    terminatorRules = state.md.block.ruler.getRules("list")

    oldParentType    = state.parentType
    state.parentType = "list"

    while nextLine < endLine:
        pos  = posAfterMarker
        _max = state.eMarks[nextLine]

        initial = state.sCount[nextLine] + posAfterMarker - (state.bMarks[nextLine] + state.tShift[nextLine])
        offset = initial

        while pos < _max:
            ch = state.src[pos]

            if ch == "\t":
                offset += 4 - (offset + state.bsCount[nextLine]) % 4
            elif ch == " ":
                offset += 1
            else:
                break
            pos += 1

        contentStart      = pos
        indentAfterMarker = None

        if contentStart >= _max:
            # trimming space in "-    \n  3" case, indent is 1 here
            indentAfterMarker = 1
        else:
            indentAfterMarker = offset - initial

        # If we have more than 4 spaces, the indent is 1
        # (the rest is just indented code block)
        if indentAfterMarker > 4:
            indentAfterMarker = 1

        # "  -  test"
        #  ^^^^^ - calculating total length of this thing
        indent = initial + indentAfterMarker

        # Run subparser & write tokens
        token        = state.push('list_item_open', 'li', 1)
        token.markup = str(markerCharCode)
        itemLines    = [nextLine, 0]
        token.map    = itemLines
        if isOrdered:
            token.info = state.src[start:posAfterMarker-1]

        # change current state, then restore it after parser subcall
        oldTight  = state.tight
        oldTShift = state.tShift[nextLine]
        oldSCount = state.sCount[nextLine]

        #  - example list
        # ^ listIndent position will be here
        #   ^ blkIndent position will be here
        #
        oldListIndent    = state.listIndent
        state.listIndent = state.blkIndent
        state.blkIndent  = indent

        state.tight            = True
        state.tShift[nextLine] = contentStart - state.bMarks[nextLine]
        state.sCount[nextLine] = offset

        if contentStart >= _max and state.isEmpty(nextLine + 1):
            # workaround for this case
            # (list item is empty, list terminates before "foo"):
            # ~~~~~~~~
            #   -
            #
            #     foo
            # ~~~~~~~~
            state.line = min(state.line + 2, endLine)
        else:
            state.md.block.tokenize(state, nextLine, endLine, True)

        # If any of list item is tight, mark list as tight
        if not state.tight and prevEmptyEnd:
            tight = False

        # Item become loose if finish with empty line,
        # but we should filter last element, because it means list finish
        prevEmptyEnd = (state.line - nextLine) > 1 and state.isEmpty(state.line - 1)

        state.blkIndent        = state.listIndent
        state.listIndent       = oldListIndent
        state.tShift[nextLine] = oldTShift
        state.sCount[nextLine] = oldSCount
        state.tight            = oldTight

        token        = state.push('list_item_close', 'li', -1)
        token.markup = str(markerCharCode)

        nextLine     = state.line
        itemLines[1] = nextLine

        if nextLine >= endLine:
            break

        # Try to check if list is terminated or continued.
        if state.sCount[nextLine] < state.blkIndent:
            break

        # if it's indented more than 3 spaces, it should be a code block
        if state.sCount[nextLine] - state.blkIndent >= 4:
            break

        # fail if terminating block found
        terminate = False
        i = 0
        l = len(terminatorRules)
        while i < l:
            if terminatorRules[i](state, nextLine, endLine, True):
                terminate = True
                break
        if terminate:
            break

        # fail if list has another type
        if isOrdered:
            posAfterMarker = skipOrderedListMarker(state, nextLine)
            if posAfterMarker < 0:
                break
            start = state.bMarks[nextLine] + state.tShift[nextLine]
        else:
            posAfterMarker = skipBulletListMarker(state, nextLine)
        if posAfterMarker < 0:
            break

        if markerCharCode != state.src.charCodeAt(posAfterMarker - 1):
            break

    # Finalize list
    if isOrdered:
        token = state.push('ordered_list_close', 'ol', -1)
    else:
        token = state.push('bullet_list_close', 'ul', -1)
    token.markup = str(markerCharCode)

    listLines[1] = nextLine
    state.line   = nextLine

    state.parentType = oldParentType

    # mark paragraphs tight if needed
    if tight:
        markTightParagraphs(state, listTokIdx)

    return True


if 0:
    src = """
### markdown


- markdown is markdown
    - where is markdown
    - except from
        - indent 8
\there
- wei is wei
    """.strip()
    sb = StateBlock(src, "md", "env", "tokens")
    print("bMarks:", sb.bMarks)
    print("eMarks:", sb.eMarks)
    print("tShift:", sb.tShift)
    print("sCount:", sb.sCount)
    print("bsCount:", sb.bsCount)
    print(sb.getLines(3, 8, 0, False))

if 0:
    token = Token("paragraph_open", "p", 1)