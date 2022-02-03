import json
import sys
import copy

from count_jmp_br import count_jmp_br


def never_used_one_pass(prog_arg):
    prog = copy.deepcopy(prog_arg)  # want CBN behavior...
    # print('starting!')
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


def overwritten_before_use_one_pass(prog_arg):
    prog = copy.deepcopy(prog_arg)  # want CBN behavior...
    for func in prog['functions']:
        def_unused = {}  # defined but not yet used
        for instr in func['instrs']:

            if 'args' in instr:
                for arg in instr['args']:
                    # print(f'{arg} just got used')
                    if arg in def_unused:
                        def_unused.pop(arg)  # these args just got used

            if 'dest' in instr:
                var = instr['dest']  # we're assigning to this var
                # print(f'{var} just got assigned')
                if var in def_unused:
                    func['instrs'].remove(def_unused[var])
                def_unused[var] = instr
    return prog


def tdce():
    prog1 = json.load(sys.stdin)
    if count_jmp_br(prog1) > 0:
        sys.exit('This implementation does not support jmp/br.')
    prog2 = overwritten_before_use_one_pass(never_used_one_pass(prog1))
    while (prog1 != prog2):
        prog1 = prog2
        prog2 = overwritten_before_use_one_pass(never_used_one_pass(prog1))
    json.dump(prog1, sys.stdout)


if __name__ == '__main__':
    tdce()
