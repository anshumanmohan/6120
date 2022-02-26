from make_cfg import *
from functools import partial
import copy


def print_doms(doms, s):
    for v in doms:
        if doms[v]:
            print(f"The {s}dominators of {v} are:")
            for b in doms[v]:
                print(f"\t{b}")
        else:
            print(f"{v} has no {s}dominators.")
    print("\n")


def print_labeled_prog(label2block):
    for idx, (name, block) in enumerate(label2block):
        print(f"{name}:")
        for row in block:
            print(f"\t{row}")
    print("\n")


def init_doms(cfg):
    # start off with a complete relation,
    # mapping each vertex label to {the set of all vertex labels}
    doms = {}
    for vlabel in cfg.keys():
        doms[vlabel] = set(cfg.keys())
    return doms


def iterate_to_convergence(f, input):
    # Copied over from my Lesson 3 solution
    # Apply f to input until convergence
    output = f(input)
    # print(f"===\n{input} \nchanged into: \n{output}\n===\n")
    while (input != output):
        input = output
        output = f(input)
        # print(f"===\n{input} \nchanged into: \n{output}\n===\n")
    return output


def intersect_list_of_sets(l):
    if l:
        return l[0].intersection(*l)
    else:
        return set()


def improve_dom_one_pass(cfg, entry_label, dom):
    dom = copy.deepcopy(dom)
    for vlabel in cfg.keys():
        if vlabel == entry_label:
            dom[vlabel] = {vlabel}
        else:
            preds = list(cfg[vlabel].predecessors)
            # print(f"I am {vlabel} and my preds are: {preds}")
            pred_dom_sets = []
            for pred in preds:
                # print(f"\tI am the pred {pred} and my doms are {dom[pred]}")
                pred_dom_sets = pred_dom_sets + [dom[pred]]
                # print(f"\tThe list of pred-doms is now {pred_dom_sets}")
            dom[vlabel] = {vlabel}.union(intersect_list_of_sets(pred_dom_sets))
    return dom


def find_doms_helper(cfg, entry_label):
    f = partial(improve_dom_one_pass, cfg, entry_label)
    # fix the method to this CFG and this entry label
    doms = init_doms(cfg)
    # pare it down until it stabilizes
    return (iterate_to_convergence(f, doms))


def find_doms(func):

    # Get the basic block and CFG for this function
    blocks = form_blocks(func['instrs'])
    label2block = label_blocks(blocks)

    print("After adding labels, the program looks like:")
    print_labeled_prog(label2block)

    entry_label = label2block[0][0]
    # print(f"Its entry label is {entry_label}")

    cfg, _ = get_cfg(label2block)

    return (entry_label, find_doms_helper(cfg, entry_label))


def main():
    # Load the program JSON
    prog = json.load(sys.stdin)

    for func in prog['functions']:
        (_, doms) = find_doms(func)
        print_doms(doms, "")


if __name__ == '__main__':
    main()
