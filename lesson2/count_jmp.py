import json
import sys


def count_jmp():
    count = 0
    prog = json.load(sys.stdin)
    for func in prog['functions']:
        for instr in func['instrs']:
            if 'op' in instr and instr['op'] == 'jmp':
                count = count + 1
    print(count)


if __name__ == '__main__':
    count_jmp()
