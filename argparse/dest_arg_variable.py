import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-l', type = int, default = 3, metavar='length')
parser.add_argument('-m', type = int, default = 21, dest='mode')    #  只能通过 args.mode 访问该参数，不能通过 args.m 访问该参数
parser.print_help()

arg = parser.parse_args()

print(arg.l)
print(arg.mode)     # dest="mode"
print(arg.m)        # @ERROR: AttributeError: 'Namespace' object has no attribute 'm'
#>> python dest_arg_variable.py