import json
import sys


def tdce_one_pass(prog):
    for func in prog['functions']:
        used = set()
        for instr in func['instrs']:
            if 'args' in instr:
                for arg in instr['args']:
                    used.add(arg)
        for instr in func['instrs']:
            if ('dest' in instr and instr['dest'] not in used):
                func['instrs'].remove(instr)
    return prog


def tdce():
    prog1 = json.load(sys.stdin)
    prog2 = tdce_one_pass(prog1)
    while (prog1 != prog2):
        prog1 = prog2
        prog2 = tdce_one_pass(prog1)
    json.dump(prog1, sys.stdout)


if __name__ == '__main__':
    tdce()
