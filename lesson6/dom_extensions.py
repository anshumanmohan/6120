from dom import *


def print_dom_frontier(doms):
    for v in doms:
        if doms[v]:
            print(f"The dominance frontier of {v} is:")
            for b in doms[v]:
                print(f"\t{b}")
        else:
            print(f"{v} has no blocks in its dominance frontier.")
    print("\n")


def find_strict_doms(doms):
    doms = copy.deepcopy(doms)
    for label in doms:
        doms[label] = doms[label] - {label}
    return doms


def does_not_strictly_dom_any_strict_dom(strict_doms, v1, v2):
    for dom in strict_doms[v2]:
        if v1 in strict_doms[dom]:
            return False
    return True


def find_immediate_doms(strict_doms):
    immediate_doms = {}
    for v1 in strict_doms:
        for v2 in strict_doms:  # v2 = body, v1 = loop
            # print(f"Checking if {v1} is the idom of {v2}")
            if v1 in strict_doms[v2] and does_not_strictly_dom_any_strict_dom(strict_doms, v1, v2):
                if v2 in immediate_doms.keys():
                    immediate_doms[v2] = immediate_doms[v2].union({v1})
                    # print(f"\tit is!")
                else:
                    immediate_doms[v2] = {v1}
                    # print(f"\tit is!")
    return immediate_doms


def dominates_a_pred(cfg, doms, v1, v2):
    # does there exist some v3, such that v1 dominates v3 and v3 is in the preds of v2?
    v3_candidates = list(cfg[v2].predecessors)
    for v3 in v3_candidates:
        if v1 in doms[v3]:
            return True
    return False


def find_dom_frontier(cfg, doms, strict_doms):
    dom_frontier = {}
    for v1 in strict_doms:
        for v2 in strict_doms:
            if (v1 not in strict_doms[v2] and dominates_a_pred(cfg, doms, v1, v2)):
                if v1 in dom_frontier.keys():
                    dom_frontier[v1] = dom_frontier[v1].union({v2})
                else:
                    dom_frontier[v1] = {v2}
    return dom_frontier


def main():
    # Load the program JSON
    prog = json.load(sys.stdin)

    for func in prog['functions']:
        (entry_label, cfg, doms) = find_doms(func)
        strict_doms = find_strict_doms(doms)
        print_doms(strict_doms, "strict ")
        immediate_doms = find_immediate_doms(strict_doms)

        print(
            f"{entry_label} is the entry label and therefore has no immediate dominator")
        print_doms(immediate_doms, "immediate ")

        dom_frontier = find_dom_frontier(cfg, doms, strict_doms)
        print_dom_frontier(dom_frontier)


if __name__ == '__main__':
    main()
