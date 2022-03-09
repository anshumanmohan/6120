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
    ret = list(vars)
    ret.sort()
    return ret


def get_var2blocks(label2block, vars):
    defs = {}
    # a dictionary, where
    # key = a variable string
    # value = a list of block-labels for blocks that assign to v
    for var in vars:
        for label, block in label2block.items():
            for instr in block:
                if 'dest' in instr and instr['dest'] == var:
                    # we found a defn of var
                    if var in defs:
                        defs[var].append(label)
                    else:
                        defs[var] = [label]
    return defs


def flatten(t):
    return [item for sublist in t for item in sublist]


def add_phi_nodes(func, df, label2block):

    vars = get_vars(func)
    var2blocks = get_var2blocks(label2block, vars)

    for v in vars:
        for d in var2blocks[v]:
            touched = []
            # we mustn't add v-flavored phi nodes to the same d twice
            if d in df:
                for blocklabel in df[d]:
                    if blocklabel in touched:
                        continue
                    else:
                        touched.append(blocklabel)

                        # we're assuming that instruction 0 is the label
                        # and so we want to go in as instruction 1.
                        if 'op' in label2block[blocklabel][1] and \
                                label2block[blocklabel][1]['op'] == 'phi' and \
                                label2block[blocklabel][1]['dest'] == v:
                            # someone has put a phi node there but it wasn't us.
                            # we'll grow the arg and label lists of the phi node.
                            phi_instr = label2block[blocklabel][1]
                            phi_instr['labels'].append(d)
                            phi_instr['args'].append(v)
                            # print(
                            # f"Expanded an old {v}-flavored phi node in {blocklabel}")
                        else:
                            # there isn't a phi node there at all.
                            phi_instr = {"args": [v],
                                         "dest": v,
                                         "labels": [d],
                                         "op": "phi",
                                         "type": "int"
                                         }
                            # create it, add it as instr #1
                            label2block[blocklabel] = [label2block[blocklabel][0]] + \
                                [phi_instr] + label2block[blocklabel][1:]
                            # print(
                            # f"Added a new {v}-flavored phi node to {blocklabel}")
                    if blocklabel not in var2blocks[v]:
                        var2blocks[v].append(blocklabel)
    return label2block


def replace_if_possible(var2stack, var):
    if var in var2stack:
        return var2stack[var][-1]
    else:
        return var


def rename(blocklabel, cfg, label2block, var2stack, idom, ctr):
    stashstacks = copy.deepcopy(var2stack)
    block = label2block[blocklabel]
    for instr in block:
        print(instr)
        if 'args' in instr:
            instr['args'] = \
                list(map(lambda arg: replace_if_possible(
                    var2stack, arg), instr['args']))
            # replace each arg with the top-of-stack value for that arg
        if 'dest' in instr:
            ctr = ctr + 1
            newname = instr['dest'] + str(ctr)
            if instr['dest'] in var2stack:
                var2stack[instr['dest']].append(newname)
            else:
                var2stack[instr['dest']] = [newname]
            instr['dest'] = newname
            print(f"\tNew instr locally: {instr}")

            # replace dest with a new name for dest, log it in the stack
    for succlabel in list(cfg[blocklabel].successors):
        for instr in label2block[succlabel]:
            if 'op' in instr and instr['op'] == 'phi':
                # this is a phi node.
                # if our stack has a value for one of its args, we'll update it.
                # but we'll only do it once per phi node...
                # print(instr)
                for i in range(len(instr['args'])):
                    if instr['args'][i] in var2stack:
                        # print(
                        # f"Will replace {instr['args'][i]} with {var2stack[instr['args'][i]][-1]}")
                        instr['args'][i] = var2stack[instr['args'][i]][-1]
                        break
                print(f"New instr in my successor: {instr}")
    if blocklabel in idom:
        for idomlabel in idom[blocklabel]:
            ctr = ctr + 1
            rename(idomlabel, cfg, label2block, var2stack, idom, ctr)
    var2stack = copy.deepcopy(stashstacks)


def remove_singleton_phi_nodes(label2block):
    for _, block in label2block.items():
        for instr in block:
            if 'op' in instr and \
                instr['op'] == 'phi' and \
                    len(instr['args']) == 1:
                block.remove(instr)


def main():
    # Load the program JSON
    prog = json.load(sys.stdin)

    for i in range(len(prog['functions'])):
        func_i = prog['functions'][i]
        (entry_label, _, doms) = find_doms(func_i)
        strict_doms = find_strict_doms(doms)
        blocks = form_blocks(func_i['instrs'])
        cfg, label2block = get_cfg(label_blocks(blocks))
        # the cfg of the function, and a dict from label to block
        df = find_dom_frontier(cfg, doms, strict_doms)

        label2block = add_phi_nodes(func_i, df, label2block)

        remove_singleton_phi_nodes(label2block)
        remove_singleton_phi_nodes(label2block)

        var2stack = {}
        if 'args' in func_i:
            for arg in func_i['args']:
                var2stack[arg['name']] = [arg['name']]

        idom_flipped = find_immediate_doms(strict_doms)
        # idom_flipped[me] = who immediately dominates me
        # we need a flipped version
        idom = {}
        for child, parent in idom_flipped.items():
            parent = list(parent)[0]  # we know this is unique
            if parent in idom:
                idom[parent].append(child)
            else:
                idom[parent] = [child]

        rename(entry_label, cfg, label2block, var2stack, idom, 0)

        new_instrs = flatten(list(label2block.values()))
        prog['functions'][i]['instrs'] = new_instrs
        # assuming that the rename operation has changed label2block in place

    json.dump(prog, sys.stdout)


if __name__ == '__main__':
    main()
