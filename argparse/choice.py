import argparse

parser = argparse.ArgumentParser(description='program')
# 使用 choices 参数来限制用户只能选择特定的值。
parser.add_argument('--color', choices=['red', 'blue', 'green'])
parser.print_help()

arg = parser.parse_args()