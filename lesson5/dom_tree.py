from dom import *


def find_strict_doms(func):
    doms = find_dominators(func)
    for label in doms:
        doms[label] = doms[label] - {label}
    return doms


def main():
    # Load the program JSON
    prog = json.load(sys.stdin)

    for func in prog['functions']:
        strict_doms = find_strict_doms(func)
        print_doms(strict_doms)


if __name__ == '__main__':
    main()
