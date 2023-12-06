#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 23 Day 1 - Trebuchet?! """

from paoc.helper import get_input, print_summary
import re


def find_calibration_value(calibration_document: list[str], allow_spelled = False) -> int:
    """ https://adventofcode.com/2023/day/1 """
    
    spelled = ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')

    if allow_spelled:
        expression = r'(?=('             # allows for overlap (eightwo -> [eight, two])
        expression += r'\d|'             # actual digits OR
        expression += '|'.join(spelled)  # spelled out digits separated by | (OR)
        expression += '))'               # close two brackets opened at start
    else:
        expression = r'\d'               # only actual digits

    calibration_value = 0
    for line in calibration_document:
        hits = re.findall(expression, line)
        first, last = map(lambda x: int(x) if x.isdigit() else spelled.index(x) + 1, (hits[0], hits[-1]))
        calibration_value += first * 10 + last

    return calibration_value

def p1() -> any:
    calibration_document = get_input(1)
    return find_calibration_value(calibration_document)
    
def p2() -> any:
    calibration_document = get_input(1)
    return find_calibration_value(calibration_document, allow_spelled=True)


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
