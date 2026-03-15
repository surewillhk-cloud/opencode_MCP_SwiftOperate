import sys


def print_banner():
    # 定义颜色代码
    white = "\033[97;1m"
    yellow = "\033[33;1m"
    gray = "\033[90m"
    reset = "\033[0m"

    # 经过修正拼写并增加右下方 3D 阴影（RetroBoard 风格）的 Smart U
    # 顶部是白色主体，右侧和下方是阴影字符
    banner = r"""
  ____                       _     _   _ 
 / ___| _ __ ___   __ _ _ __| |_  | | | |
 \___ \| '_ ` _ \ / _` | '__| __| | | | |
  ___) | | | | | | (_| | |  | |_  | |_| |
 |____/|_| |_| |_|\__,_|_|   \__|  \___/ 
                                         """

    sys.stdout.write(white + banner + reset + "\n")
    sys.stdout.write(yellow + "  🟡 LLM Agent Team  v1.0" + reset + "\n")
    sys.stdout.write(
        gray + "  Dynamic Model | Parallel Exec | Auto-Security" + reset + "\n"
    )
    sys.stdout.flush()
