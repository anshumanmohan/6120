import json
import sys
import pandas as pd
from count_jmp_br import count_jmp_br
from tdce import *
from tabulate import tabulate


def get_val_and_home(table, index):
    # given the index, return the value and the home on that row
    return (table.at[index, 'value'], table.at[index, 'home'])


def get_index_and_home(table, value):
    # given the value, return the row number and the home
    # note that this is unique because we are carefully keeping it so;
    # Python makes no guarantee of uniquenes
    row = table.loc[table['value'] == value]
    # print('looking for value in table:')
    # print(value)
    assert row.shape[0] == 1  # check that we got a single-row table
    index = row.index.values[0]
    return (index, row.at[index, 'home'])


def add_row_to_table(table, value, home):
    new = pd.DataFrame([[value, home]], columns=['value', 'home'])
    return pd.concat([table, new])


def lvn_one_pass(prog):
    for func in prog['functions']:
        # A value_tuple is:
        # a list n+1 long:
        #   a string op code, and
        #   n integers representing table row numbers for the arguments
        table = pd.DataFrame(columns=['value', 'home'])
        # In each row: value_tuple, its string home
        cloud = {}  # a dict from string varname to its int row number in table

        for instr in func['instrs']:

            if 'label' in instr:
                # we screen away jmp and br, so we can just ignore labels
                continue

            op = instr['op']

        # we construct the value tuple with references to row numbers
            if op == 'const':
                # special-casing this
                value = (op, instr['value'])
            else:
                value = (op,)
                if 'args' in instr:
                    for arg in instr['args']:
                        value = value + (cloud[arg],)

            if table.shape[0] > 0 and True in table['value'].isin([value]).values:
                # this very value has been computed in the past
                # print("I think the value")
                # print(value)
                # print(" is in table ")
                # print(tabulate(table))
                (index, home) = get_index_and_home(table, value)
                # it lives here!
                new_instr = {'args': [home], 'op': 'id'}
                # hopefully this is kosher json...

            else:
                # this is a new value
                if 'dest' in instr:
                    dest = instr['dest']

                    # if variable will be overwritten...
                    # pass

                    # add it to the table
                    table = add_row_to_table(table, value, dest)
                    row = table.shape[0]  # here's where it went

                    if op == 'const':
                        new_instr = instr
                    else:
                        new_instr = {'args':
                                     map((lambda a: table['homes'][cloud[a]]),
                                         instr['args']),
                                     'op': op}

            # regardless:
            if 'dest' in instr:
                cloud[instr['dest']] = row  # housekeep the cloud
            instr = new_instr  # hopefully this edit is in-place...

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
