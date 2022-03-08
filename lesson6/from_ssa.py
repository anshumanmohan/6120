from dom import *
from dom_extensions import *
import copy


def from_ssa(func):
    return func


def main():
    # Load the program JSON
    prog = json.load(sys.stdin)

    for func in prog['functions']:
        from_ssa(func)

    json.dump(prog, sys.stdout)


if __name__ == '__main__':
    main()
