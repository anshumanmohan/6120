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


def to_ssa(func):
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
                        # label2block[blocklabel].append
                        # {'args': [val_i],
                        #  'dest': instr['dest'],
                        #  'op': 'id',
                        #  'type': instr['type']}
                        print(f"Added a {v}-flavored phi node to {blocklabel}")
                    if blocklabel not in var2blocks[v]:
                        var2blocks[v].append(blocklabel)
    return flatten(list(label2block.values()))


def main():
    # Load the program JSON
    prog = json.load(sys.stdin)

    for i in range(len(prog['functions'])):
        func_i = prog['functions'][i]
        prog['functions'][i]['instrs'] = to_ssa(func_i)


if __name__ == '__main__':
    main()
