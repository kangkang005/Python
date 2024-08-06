import argparse

parser = argparse.ArgumentParser(description='input export')
parser.add_argument('input', type=str, help='input')
parser.add_argument('export', type=str, help='export')
args = parser.parse_args()

#打印姓名
print(args.input + "_" + args.export)