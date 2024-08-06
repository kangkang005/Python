import argparse

parser = argparse.ArgumentParser(description='program')
parser.add_argument('-m', '--mode', type=str, default="normal", help='which mode')
parser.add_argument('-i', '--input', type=str, required=True, help='input file')
args = parser.parse_args()

print(args.mode)
print(args.input)
#>> python requirement.py