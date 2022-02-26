from dom import *


def find_strict_doms(doms):
    doms = copy.deepcopy(doms)
    for label in doms:
        doms[label] = doms[label] - {label}
    return doms


def find_immediate_doms(strict_doms):
    immediate_doms = {}
    for v1 in strict_doms:
        for v2 in strict_doms:
            if v1 in strict_doms[v2] and (v1 not in strict_doms[v3] for v3 in strict_doms[v2]):
                # ...
                if v2 in immediate_doms.keys():
                    immediate_doms[v2] = immediate_doms[v2].union({v1})
                else:
                    immediate_doms[v2] = {v1}
    return immediate_doms


def main():
    # Load the program JSON
    prog = json.load(sys.stdin)

    for func in prog['functions']:
        (entry_label, doms) = find_doms(func)
        strict_doms = find_strict_doms(doms)
        print_doms(strict_doms, "strict ")
        immediate_doms = find_immediate_doms(strict_doms)

        print(
            f"{entry_label} is the entry label and therefore has no immediate dominators")
        print_doms(immediate_doms, "immediate ")


if __name__ == '__main__':
    main()
