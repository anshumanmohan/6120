import json
import sys
import pandas as pd
from count_jmp_br import count_jmp_br
from tdce import *
from tabulate import tabulate

# DATAFRAME ACCESS, MODIFICATION, HELPERS


def get_val_and_home(table, index):
    # given the index, return the value and the home on that row
    return (table.at[index, 'value'], table.at[index, 'home'])


def get_index_and_home(table, value):
    # given the value, return the row number and the home
    # note that this is unique because we are carefully keeping it so;
    # Python makes no guarantee of uniquenes
    row = table.loc[table['value'] == value]
    assert row.shape[0] == 1  # check that we got a single-row table
    index = row.index.values[0]
    return (index, row.at[index, 'home'])


def add_row_to_table(table, value, home):
    len = table.shape[0]
    new = pd.DataFrame([[value, home]], index=[len], columns=['value', 'home'])
    table = pd.concat([table, new])
    return table


def row_is_const(table, index):
    value, _ = get_val_and_home(table, index)
    return value[0] == 'const'


def get_const(table, index):
    value, _ = get_val_and_home(table, index)
    assert value[0] == 'const'
    return value[1][0]


def canonicalize(value):
    op = value[0]
    rest = value[1:]
    if op in ['add', 'mul']:
        rest = sorted(rest)
    return (op,) + (rest,)


def do_math(table, value, instr):
    # do math on constants if possible
    op = value[0]
    rest = value[1:]
    if op in ['add', 'mul', 'sub', 'div'] and row_is_const(table, rest[0][0]) and row_is_const(table, rest[0][1]):
        arg1 = get_const(table, rest[0][0])
        arg2 = get_const(table, rest[0][1])
        if op == 'add':
            ans = arg1 + arg2
        elif op == 'mul':
            ans = arg1 * arg2
        elif op == 'sub':
            ans = arg1 - arg2
        else:
            ans = arg1 / arg2
        # short-circuit the value and the instr; just use constants
        value = ('const', [ans])
        instr = {'dest': instr['dest'],
                 'op': 'const',
                 'type': instr['type'],
                 'value': ans}

    if op == 'id' and row_is_const(table, rest[0][0]):
        ans = get_const(table, rest[0][0])
        # short-circuit the value and the instr; just use constants
        value = ('const', [ans])
        instr = {'dest': instr['dest'],
                 'op': 'const',
                 'type': instr['type'],
                 'value': ans}

    return (value, instr)


def lvn_one_pass(prog):
    for func in prog['functions']:
        # After canonicalization, a value_tuple is:
        # a string op code, and
        # a list of n integers representing table row numbers for the arguments
        table = pd.DataFrame()
        # In each row: value_tuple, its string home
        cloud = {}  # a dict from string varname to its int row number in table

        for i in range(len(func['instrs'])):

            instr = func['instrs'][i]

            if 'label' in instr:
                # we've screened away jmp and br,
                # so we can just leave labels untouched
                continue

            if 'dest' not in instr:
                # If it doesnt have a dest, it can't add to the table/cloud
                # Just rewrite it according to the table/cloud as they are

                assert instr['op'] == 'print'  # AFAIK, only print has no dest
                arg = instr['args'][0]
                row = cloud[arg]
                _, home = get_val_and_home(table, row)
                new_instr = {'args': [home], 'op': 'print'}
                func['instrs'][i] = new_instr
                continue

            op = instr['op']
            dest = instr['dest']

            # we construct the value tuple with references to row numbers
            if op == 'const':
                value = (op, [instr['value']])  # special-casing this
            else:
                value = (op,)
                if 'args' in instr:
                    for arg in instr['args']:
                        value = value + (cloud[arg],)
                value = canonicalize(value)

            if table.shape[0] > 0 and True in table['value'].isin([value]).values:
                # if this very value has been computed in the past
                (row, home) = get_index_and_home(table, value)
                # we find where it lives
                # and replace it with an id instr
                new_instr = {'args': [home],
                             'dest': dest,
                             'op': 'id',
                             'type': instr['type']}

            else:
                # this is a new value

                # do math simplifications if possible
                (value, instr) = do_math(table, value, instr)
                # note the in-place clobber

                # if dest var will be overwritten, rename it prophylactically
                for j in range(i+1, len(func['instrs'])):
                    future_instr = func['instrs'][j]
                    if 'dest' in future_instr and future_instr['dest'] == dest:
                        dest = dest + "'"
                        break  # break out of this j-forloop

                # add it to the table
                table = add_row_to_table(table, value, dest)
                row = table.shape[0]-1  # here's where it went

                # now we'll "pretty print" the new instr
                # by reading from the cloud and the table
                if instr['op'] == 'const':
                    new_instr = instr
                else:
                    new_instr = {'args':
                                 list(map((lambda a: table['home'][cloud[a]]),
                                          instr['args'])),
                                 'dest': dest,
                                 'op': op,
                                 'type': instr['type']}

            # regardless of whether the value was old or new:
            cloud[instr['dest']] = row  # housekeep the cloud

            # print(f"\nFinished with {instr}")
            # print(f"The cloud now looks like:{cloud}")
            # print(f"The table now looks like:\n{tabulate(table)}")
            # if instr != new_instr:
            #     print(f"The instr now looks like:{new_instr}")

            func['instrs'][i] = new_instr

    return prog


def try_everything_one_pass(prog_arg):
    # In this method we will list all our strategies
    # One pass only: iterate this method to convergence!
    prog = copy.deepcopy(prog_arg)  # want CBN behavior
    overwritten_before_use_one_pass(never_used_one_pass(lvn_one_pass(prog)))
    return prog


def iterate_to_convergence(f, input):
    # Apply f to input until convergence
    output = f(input)
    while (input != output):
        input = output
        output = f(input)
    return output


def lvn():
    prog = json.load(sys.stdin)
    if count_jmp_br(prog) == 0:
        # This implementation does not support jmp/br.
        # The meat of the algorithm is only implemented once we're sure
        # we're free of these kinds of control flow.
        # In other cases, we simply return the original program.
        prog = iterate_to_convergence(try_everything_one_pass, prog)

    json.dump(prog, sys.stdout)


if __name__ == '__main__':
    lvn()
