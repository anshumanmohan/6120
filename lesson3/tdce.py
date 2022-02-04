import json
import sys
import copy

from count_jmp_br import count_jmp_br


def never_used_one_pass(prog):
    for func in prog['functions']:
        used = set()
        for instr in func['instrs']:
            if 'args' in instr:
                for arg in instr['args']:  # someone uses arg
                    used.add(arg)
        for instr in func['instrs']:
            if ('dest' in instr and instr['dest'] not in used):
                # some var is being set but no one needs it
                func['instrs'].remove(instr)  # the instr is expendable
    return prog


def overwritten_before_use_one_pass(prog):
    for func in prog['functions']:
        def_unused = {}  # defined but not used
        # a dict from a var to the instr that defines that var

        for instr in func['instrs']:

            if 'args' in instr:
                for arg in instr['args']:
                    # arg is being used in this instr
                    if arg in def_unused:
                        def_unused.pop(arg)
                        # so we prune to maintain invariant

            if 'dest' in instr:
                var = instr['dest']  # we're assigning to this var
                # print(f'{var} just got assigned')
                if var in def_unused:
                    # is this in face a _reassignent_,
                    # w/o any use of the previous assignment?
                    func['instrs'].remove(def_unused[var])
                    # if yes, its previous definition is expendable
                def_unused[var] = instr
                # regardless, this instr _is_ a definition,
                # so we add to def_unused to maintain invariant
    return prog


def try_everything_one_pass(prog_arg):
    # In this method we will list all our strategies
    # One pass only: iterate this method to convergence!
    prog = copy.deepcopy(prog_arg)  # want CBN behavior
    overwritten_before_use_one_pass(never_used_one_pass(prog))
    return prog


def iterate_to_convergence(f, input):
    # Apply f to input until convergence
    output = f(input)
    while (input != output):
        input = output
        output = f(input)
    return output


def tdce():
    prog = json.load(sys.stdin)
    if count_jmp_br(prog) == 0:
        # This implementation does not support jmp/br.
        # The meat of the algorithm is only implemented once we're sure
        # we're free of these kinds of control flow.
        # In other cases, we simply return the original program.
        prog = iterate_to_convergence(try_everything_one_pass, prog)
    json.dump(prog, sys.stdout)


if __name__ == '__main__':
    tdce()
