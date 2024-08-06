from jinja2 import *

env = Environment(
    loader                = FileSystemLoader("."),
    variable_start_string = "($",
    variable_end_string   = "$)",
    undefined             = StrictUndefined,
)

data = {
    "heading"  : "Welcome",
    "name"     : "Student",
    "item_list": ["apple", "orange", "banana"],
    "count"    : 8,
}

template = env.get_template("template.txt")

try:
    result = template.render(data)
    print(result)
except Exception as e:
    print(e)