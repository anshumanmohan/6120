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
    len = table.shape[0]
    new = pd.DataFrame([[value, home]], index=[len], columns=['value', 'home'])
    table = pd.concat([table, new])
    return table


def lvn_one_pass(prog):
    for func in prog['functions']:
        # A value_tuple is:
        # a list n+1 long:
        #   a string op code, and
        #   n integers representing table row numbers for the arguments
        table = pd.DataFrame()
        # In each row: value_tuple, its string home
        cloud = {}  # a dict from string varname to its int row number in table

        for i in range(len(func['instrs'])):

            instr = func['instrs'][i]
            # print(f"processing instruction {instr}")

            if 'label' in instr:
                # we've screened away jmp and br, so we can just ignore labels
                continue

            if 'dest' not in instr:
                # If it doesnt have a dest, it can't add to the table/cloud
                # Just rewrite it according to the table/cloud as it stands

                # so far, only print has no dest...
                assert instr['op'] == 'print'
                arg = instr['args'][0]
                row = cloud[arg]
                _, home = get_val_and_home(table, row)
                new_instr = {'args': [home],
                             'op': 'print'}
                func['instrs'][i] = new_instr
                # print(f"I'm gonna replace {instr} with {new_instr}")
                continue

            op = instr['op']
            dest = instr['dest']

            # we construct the value tuple with references to row numbers
            if op == 'const':
                value = (op, instr['value'])  # special-casing this
            else:
                value = (op,)
                if 'args' in instr:
                    for arg in instr['args']:
                        # print(f"Gonna look in the cloud re: instr {instr}")
                        value = value + (cloud[arg],)

            if table.shape[0] > 0 and True in table['value'].isin([value]).values:
                # print(f"I think {value} is precomputed in \n{tabulate(table)}")

                # this very value has been computed in the past
                (index, home) = get_index_and_home(table, value)
                # and it lives here!

                new_instr = {'args': [home],
                             'dest': dest,
                             'op': 'id',
                             'type': instr['type']}
                # print(f"I'm gonna replace {instr} with {new_instr}")

            else:
                # this is a new value

                # if variable will be overwritten...
                # pass

                # add it to the table
                table = add_row_to_table(table, value, dest)
                row = table.shape[0]-1  # here's where it went

                if op == 'const':
                    new_instr = instr
                else:
                    new_instr = {'args':
                                 list(map((lambda a: table['home'][cloud[a]]),
                                          instr['args'])),
                                 'dest': dest,
                                 'op': op,
                                 'type': instr['type']}

            # regardless:
            # print(f"housekeeping cloud for {instr}")
            cloud[dest] = row  # housekeep the cloud
            # print(f"The cloud now looks like:{cloud}")
            # print(f"The table now looks like:\n{tabulate(table)}")

            func['instrs'][i] = new_instr
            # print(func)

    # print("RETURNING")
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
        # print("ITERATING AGAIN")
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
