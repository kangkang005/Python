from jinja2 import Template

# 模板字符串
template_string = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ heading }}</h1>
    <p>Hello, {{ name }}!</p>

    <!-- for -->
    # 当你在块（比如一个 for 标签、一段注释或变量表达式）的开始或结束放置一个减号（ - ），可以移除块前或块后的空白:
    <ul>
    {%- for item in item_list %}
        <li>{{ item }}</li>
    {%- endfor %}
    </ul>

    <!-- if -->
    {%- if count > 10 %}
        <p>There are too many items.</p>
    {%- else %}
        <p>There are {{ count }} items.</p>
    {%- endif %}
</body>
</html>
"""

# 创建模板对象
template = Template(template_string)

data = {
    "title"    : "My Title",
    "heading"  : "Welcome",
    "name"     : "Student",
    "item_list": ["apple", "orange", "banana"],
    "count"    : 8,
}

# 渲染模板
print(template.render(data))