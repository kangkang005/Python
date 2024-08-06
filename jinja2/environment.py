from jinja2 import Environment, Template, FileSystemLoader

env = Environment(
    loader                = FileSystemLoader("."),
    block_start_string    = "(%",
    block_end_string      = "%)",
    variable_start_string = "($",
    variable_end_string   = "$)",
    comment_start_string  = "(#",
    comment_end_string    = "#)",
    # 开启缩进, 无需在块标签中放置一个减号（ - ），
    trim_blocks           = True,
    lstrip_blocks         = True,
    # 移除 jinja2 模板中的尾随换行符
    keep_trailing_newline = False,
)

template = env.get_template("template.txt")

data = {
    "title"    : "My Title",
    "heading"  : "Welcome",
    "name"     : "Student",
    "item_list": ["apple", "orange", "banana"],
    "count"    : 8,
}

# 渲染模板
print(template.render(data))