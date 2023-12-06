#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 22 Day 10 - Cathode-Ray Tube """

from paoc.helper import get_input, print_summary


def p1() -> any:
    
    lines = get_input(10)
    history: list[int] = [1]

    for line in lines:
        if line.startswith('noop'):
            # add one record to history with same value as before
            history.append(history[-1])
        else:
            V = int(line.strip().split(' ')[-1])
            # after the first cycle, nothing has changed
            history.append((last:=history[-1]))
            # after the second cycle, we increment the register with V
            history.append(last+V)

    # remove the first entry in history, as it was not part of the clock cycles we needed to track
    history = history[1:]

    signal_strengths = 0
    # history[18] reflects the state of the register *after* the 19th clock cycle (i.e. during the 20th cycle)
    for i in range(18, len(history), 40):
        signal_strengths += history[i] * (i+2)

    return signal_strengths

def p2() -> any:
    
    lines = get_input(10)
    history: list[int] = [1]

    for line in lines:
        if line.startswith('noop'):
            # add one record to history with same value as before
            history.append(history[-1])
        else:
            V = int(line.strip().split(' ')[-1])
            # after the first cycle, nothing has changed
            history.append((last:=history[-1]))
            # after the second cycle, we increment the register with V
            history.append(last+V)

    # remove the last entry in history, as we are only interested in the register state *during* a given cycle
    history = history[:-1]

    # render screen by looping over the history in chunks of 40
    screen: str = ''
    for i in range(0, len(history), 40):
        screen += '\n' + ''.join(['#' if (abs(history[i:i+40][p]-p) < 2) else '.' for p in range(40)])
    return screen


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
