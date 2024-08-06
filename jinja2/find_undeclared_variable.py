from jinja2 import Environment, FileSystemLoader, StrictUndefined, meta

env = Environment(
    loader                = FileSystemLoader("."),
    variable_start_string = "($",
    variable_end_string   = "$)",
    undefined             = StrictUndefined,
)

with open("template.txt", "r", encoding='UTF-8') as r_temp:
    txt = r_temp.read()

# print(list(env.lex(txt)))
ast = env.parse(txt)
print(list(meta.find_undeclared_variables(ast)))