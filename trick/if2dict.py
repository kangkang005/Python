print("########### if style ############")
name = "spectre"
tool = ""
if name == "spectre":
    tool = "use_spectre_tool"
elif name == "hspice":
    tool = "use_hspice_tool"
print(tool)


print("########### dict style ############")
name = "spectre"
tool = {
    "spectre": "use_spectre_tool",
    "tool"   : "use_hspice_tool",
}[name]
print(tool)