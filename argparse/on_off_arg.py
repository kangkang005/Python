import argparse

parser = argparse.ArgumentParser()
# store_true 就代表着一旦指令里写了这个参数，那么将其值设为 True，没有时，默认状态下其值为 False。同理：store_false 代表一旦命令中有此参数，其值则变为 False，默认为 True。
parser.add_argument(
        "--on",
        dest    = "on",
        action  = "store_true",    # 写了--on，那么 on = True，否则为False
        default = False,
        help    = "If set, It will be on",
    )
parser.add_argument(
        "--off",
        action  = "store_false",    # 写了--off，那么 off = False，否则为True
        default = True,
        help    = "If set, It will be off",
    )
args = parser.parse_args()
print(args)
print(args.on)
print(args.off)

#>> python on_off_arg.py --on --off
#>> python on_off_arg.py --on
#>> python on_off_arg.py --off
#>> python on_off_arg.py