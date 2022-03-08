from dom import *
from dom_extensions import *
import copy


def get_vars(func):
    vars = set()
    # a set of the variables defined in this function
    for instr in func['instrs']:
        if 'dest' in instr:
            var = instr['dest']
            vars.add(var)
    return list(vars)


# def get_var2blocks(func):

    # defs = {}
    # a dictionary, where
    # key = a variable string
    # value = a list of block-labels for blocks that assign to v


def to_ssa(func):
    return func


def main():
    # Load the program JSON
    prog = json.load(sys.stdin)

    for func in prog['functions']:
        to_ssa(func)

    json.dump(prog, sys.stdout)


if __name__ == '__main__':
    main()
