import sys
import re
from .anjuke import community as anjuke_community
from .juejin import posts as juejin_posts
from .juejin import books as juejin_books
from . import __version__

def _print_welcom():
    print('=========================================\nHi, guy! Welcome to use kcrwaler v{} !\nhttps://github.com/kenblikylee/kcrawler\n-----------------------------------------'.format(__version__))

def _print_run(app, ver):
    _print_welcom()
    print('run kcrawler-{}v{} ...'.format(app, ver))

_supported_apps = ['juejin', 'anjuke']

_arg_pattern = re.compile(r'--\w+')

def _parse_args(args_list):
    argk = None
    args = dict()
    targets = list()
    for arg in args_list:
        if _arg_pattern.match(arg):
            argk = arg.strip('-')
            args[argk] = ''
        elif argk:
            args[argk] = arg
            argk = None
        else:
            targets.append(arg)
    return args, targets

def init_app(app, ver, args):
    if args is None:
        args = sys.argv[1:]
    _print_run(app, ver)
    return _parse_args(args)

def juejin(args=None):
    args, targets = init_app('juejin', '0.1.0', args)
    tar = targets[0]
    if tar == 'post':
        juejin_posts.main(args)
    elif tar == 'book':
        juejin_books.main(args)
    

def anjuke(args=None):
    args, targets = init_app('anjuke', '0.1.1', args)
    anjuke_community.main(args)

def args(args=None):
    args, targets = init_app('args', '0.1.0', args)
    print(args, targets)

def main():
    cmds = sys.argv[1:]
    if len(cmds) == 0:
        _print_welcom()
        exit(0)
    app = cmds[0]
    if not app in _supported_apps:
        print('{} not supported!'.format(app))
        exit(0)
    args = cmds[1:]
    eval('{}(args)'.format(app))
