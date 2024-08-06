import argparse

my_usage = """
************************************************************
        PIQA -y <yaml name> [-m] [--mode]
************************************************************
"""
my_epilog = "****     Version 1.0 (xxxx/xx/xx)     ****"
parser = argparse.ArgumentParser(
    prog            = "PIQA",       # 程序的名称 (默认值: os.path.basename(sys.argv[0]))
    epilog          = my_epilog,    # 要在参数帮助信息之后显示的文本
    formatter_class = argparse.RawDescriptionHelpFormatter, #  用于自定义帮助文档输出格式的类
    description     = 'program',    # 要在参数帮助信息之前显示的文本
    add_help        = True,         # 为解析器添加一个 -h/--help 选项 (默认值： True)
    usage           = my_usage,     # 描述程序用途的字符串 (默认值：从添加到解析器的参数生成)
    )
parser.add_argument('-m', '--mode', type=str, default="normal", help='which mode')
parser.add_argument('-i', '--input', type=str, help='input file')
args = parser.parse_args()

print(args.mode)
print(args.input)
#>> python default.py --input test.txt