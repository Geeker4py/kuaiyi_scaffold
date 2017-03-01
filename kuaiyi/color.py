import os

'''
前景色            背景色           颜色
---------------------------------------
30                40              黑色
31                41              红色
32                42              绿色
33                43              黃色
34                44              蓝色
35                45              紫红色
36                46              青蓝色
37                47              白色
'''

def colored(text, color=None, on_color=None, attrs=None):
    fmt_str = '\x1B[;%dm%s\x1B[0m'
    if color is not None:
        text = fmt_str % (color, text)

    if on_color is not None:
        text = fmt_str % (on_color, text)

    if attrs is not None:
        for attr in attrs:
            text = fmt_str % (color, text)

    return text

def printError(msg):
    print colored(msg, color=36)

def printWarning(msg):
    print colored(msg, color=33)

def printInfo(msg):
    print colored(msg, color=37)

if __name__ == '__main__':
    printError("this is an error message!")
    printWarning("this is a warning message!")
    printInfo("this ia a info message!")
