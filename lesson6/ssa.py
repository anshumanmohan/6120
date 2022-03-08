from dom import *
from dom_extensions import *
import copy


def ssa(func):
    return func


def main():
    # Load the program JSON
    prog = json.load(sys.stdin)

    for func in prog['functions']:
        ssa(func)

    json.dump(prog, sys.stdout)


if __name__ == '__main__':
    main()
