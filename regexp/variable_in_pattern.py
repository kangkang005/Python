import re

line = "Cats are smarter than dogs"
animal = "dogs"

if re.search(rf"than\s+{animal}", line, flags=re.I):
    print("matched")