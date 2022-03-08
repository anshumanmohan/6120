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


def add_phi_nodes(func):
    blocks = form_blocks(func['instrs'])
    cfg, label2block = get_cfg(label_blocks(blocks))
    # the cfg of the function, and a dict from label to block

    (entry_label, _, doms) = find_doms(func)
    strict_doms = find_strict_doms(doms)
    df = find_dom_frontier(cfg, doms, strict_doms)

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
                            print(
                                f"Expanded an old {v}-flavored phi node in {blocklabel}")
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
                            print(
                                f"Added a new {v}-flavored phi node to {blocklabel}")
                    if blocklabel not in var2blocks[v]:
                        var2blocks[v].append(blocklabel)
    return flatten(list(label2block.values()))


def main():
    # Load the program JSON
    prog = json.load(sys.stdin)

    # adding phi nodes
    for i in range(len(prog['functions'])):
        func_i = prog['functions'][i]
        prog['functions'][i]['instrs'] = add_phi_nodes(func_i)

    json.dump(prog, sys.stdout)


if __name__ == '__main__':
    main()
