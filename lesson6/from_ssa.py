from dom import *
from dom_extensions import *
import copy


def print_labeled_prog(label2block):
    for (name, block) in label2block.items():
        # print(f"{name}:")
        for row in block:
            print(f"\t{row}")
    print("\n")


def add_instr_to_block(block, instr):
    # just adding it to the very end is not good enough;
    # we must cut ahead of any jumps or branches!
    last = block.pop()
    if 'op' in last and last['op'] in ('jmp', 'br'):
        block.append(instr)
        block.append(last)
    else:
        block.append(last)
        block.append(instr)


def flatten(t):
    return [item for sublist in t for item in sublist]


def from_ssa(func):
    blocks = form_blocks(func['instrs'])
    cfg, label2block = get_cfg(label_blocks(blocks))
    # the cfg of the function, and a dict from label to block

    for label, block in label2block.items():
        for instr in block:
            if 'op' in instr and instr['op'] == 'phi':  # we found a phi node
                # print(f"Found a phi node: {label}")
                pred_labels = list(cfg[label].predecessors)  # my preds
                for i in range(len(instr['labels'])):
                    val_i = instr['args'][i]
                    pred_i = instr['labels'][i]
                    assert pred_i in pred_labels  # sanity check
                    block_i = label2block[pred_i]
                    # now block_i needs a new instruction at the end,
                    # where val_i is assigned to instr['dest'].
                    add_instr_to_block(block_i, {'args': [val_i],
                                                 'dest': instr['dest'],
                                                 'op': 'id',
                                                 'type': instr['type']})
                    # print(f"Added {instr['dest']} := {val_i} to {pred_i}")
                    # print(f"The block now looks like: {block_i}")
                block.remove(instr)  # the present instr is expendable

    # new_func = func
    # print(label2block)
    # return func
    # print_labeled_prog(label2block)
    return flatten(list(label2block.values()))


def main():
    # Load the program JSON
    prog = json.load(sys.stdin)

    for i in range(len(prog['functions'])):
        func_i = prog['functions'][i]
        prog['functions'][i]['instrs'] = from_ssa(func_i)

    # print(prog)
    json.dump(prog, sys.stdout)


if __name__ == '__main__':
    main()
