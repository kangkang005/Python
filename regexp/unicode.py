import re

# .。．｡
REGEX_SEPARATORS = re.compile(r"[\x2E\u3002\uFF0E\uFF61]")
REGEX_NON_ASCII  = re.compile(r"[^\0-\x7E]")

split_str = REGEX_SEPARATORS.split("before。after")
print(split_str)
print("\x7E")