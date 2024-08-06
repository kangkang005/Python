# @Recursion:
#   decimal to every conversion
def decimal_conversion(n, base):
    map = "0123456789ABCDEF"
    if n < base:
        return map[n]
    return decimal_conversion(n//base, base) + map[n%base]

#   every conversion to decimal
def to_decimal(string, base, factor=0):
    map = "0123456789ABCDEF"
    if string == "":
        return 0
    return to_decimal(string[:-1], base, factor+1) + map.find(string[-1])*pow(base, factor)

res = decimal_conversion(1024, 16)
print(res)
res = to_decimal("BC", 16)
print(res)

# hex to bin
res = decimal_conversion(to_decimal("BC", 16), 2)
print(res)
# hex to oct
res = decimal_conversion(to_decimal("BC", 16), 8)
print(res)
# hex to dec
res = decimal_conversion(to_decimal("BC", 16), 10)
print(res)
# hex to hex
res = decimal_conversion(to_decimal("BC", 16), 16)
print(res)