import argparse

parser = argparse.ArgumentParser(description='input multiple arguments')
# nargs 是传入的参数个数，'+' 表示传入至少一个参数。
parser.add_argument('-i', type=str, nargs="+", help='input number')
args = parser.parse_args()

print(args)
print(args.i)   # type: list
#>> python input_single_arg.py -i 1 2 3