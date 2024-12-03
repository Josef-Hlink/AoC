#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 24 Day 3 - Mull It Over """

from paoc.helper import get_input, print_summary
import re


def p1() -> any:
    return sum(map(lambda x: int(x[0]) * int(x[1]), re.findall(r'mul\((\d+),(\d+)\)', ''.join(get_input(3)))))

def p2() -> any:
    res, enabled = 0, True
    for line in get_input(3):
        matches = re.findall(r'(mul\((\d+),(\d+)\))|(do\(\))|(don\'t\(\))', line)
        while matches:
            instr = matches.pop(0)  # instruction: [mul(x,y), x, y, do(), don't()]
            if instr[0]:  # mul; tuple looks like [mul(x,y), x, y, '', '']
                res += int(instr[1]) * int(instr[2]) * enabled
            else:  # enable/disable; tuple is ['', '', '', do(), ''] or ['', '', '', '', don't()]
                enabled = instr[3] == 'do()'
    return res


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
