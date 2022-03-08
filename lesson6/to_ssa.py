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
    blocks = form_blocks(func['instrs'])
    cfg, label2block = get_cfg(label_blocks(blocks))
    # the cfg of the function, and a dict from label to block

    print(f"The variables of this function are: {get_vars(func)}")


def main():
    # Load the program JSON
    prog = json.load(sys.stdin)

    for i in range(len(prog['functions'])):
        func_i = prog['functions'][i]
        prog['functions'][i]['instrs'] = to_ssa(func_i)


if __name__ == '__main__':
    main()
