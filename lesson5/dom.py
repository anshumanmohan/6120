from make_cfg import *
from functools import partial
import copy


def print_doms(doms):
    print("\n")
    for v in doms:
        print(f"The dominators of {v} are:")
        for b in doms[v]:
            print(f"\t{b}")


def print_labeled_prog(label2block):
    for idx, (name, block) in enumerate(label2block):
        print(f"{name}:")
        for row in block:
            print(f"\t{row}")


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


def improve_dom_one_pass(cfg, dom):
    dom = copy.deepcopy(dom)
    for vlabel in cfg.keys():
        preds = list(cfg[vlabel].predecessors)
        print(f"I am {vlabel} and my preds are: {preds}")
        pred_dom_sets = []
        for pred in preds:
            print(f"\tI am the pred {pred} and my doms are {dom[pred]}")
            pred_dom_sets = pred_dom_sets + [dom[pred]]
            print(f"\tThe running list of pred-doms is now {pred_dom_sets}")
        dom[vlabel] = {vlabel}.union(intersect_list_of_sets(pred_dom_sets))
    return dom


def find_dominators(cfg):
    f = partial(improve_dom_one_pass, cfg)  # fix the method to this CFG
    doms = init_doms(cfg)
    # pare it down until it stabilizes
    return (iterate_to_convergence(f, doms))


def main():
    # Load the program JSON
    prog = json.load(sys.stdin)

    # Do this for each function
    for func in prog['functions']:
        # Get the basic block and CFG for this function
        blocks = form_blocks(func['instrs'])
        label2block = label_blocks(blocks)

        print("After adding labels, the program looks like:")
        print_labeled_prog(label2block)

        cfg, _ = get_cfg(label2block)

        doms = find_dominators(cfg)

        print_doms(doms)


if __name__ == '__main__':
    main()
