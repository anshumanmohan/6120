import json
import sys

CTRL_FLOW = 'jmp', 'br'


def count_jmp_br(prog):
    count = 0
    for func in prog['functions']:
        for instr in func['instrs']:
            if 'op' in instr and instr['op'] in CTRL_FLOW:
                count = count + 1
    return count
