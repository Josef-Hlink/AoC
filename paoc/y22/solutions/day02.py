#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 22 Day 2 - Rock Paper Scissors """

from paoc.helper import get_input, print_summary


def outcome1(theirs: str, ours: str) -> int:
    
    r, p, s = 'A', 'B', 'C'  # their moves
    R, P, S = 'X', 'Y', 'Z'  # our moves
    
    # we assume draw at the start
    score = 3
    if ours == R:
        if theirs == s: score = 6
        elif theirs == p: score = 0
        score += 1
    elif ours == P:
        if theirs == r: score = 6
        elif theirs == s: score = 0
        score += 2
    elif ours == S:
        if theirs == p: score = 6
        elif theirs == r: score = 0
        score += 3
    return score

def outcome2(theirs: str, ours: str) -> int:
    
    global wins, losses
    r, p, s = 'A', 'B', 'C'  # moves
    L, D, W = 'X', 'Y', 'Z'  # outcomes

    shape_scores = {r: 1, p: 2, s: 3}
    outcome_scores = {L: 0, D: 3, W: 6}

    loss = {r: s, p: r, s: p}
    draw = {r: r, p: p, s: s}
    win = {r: p, p: s, s: r}

    our_shape = {L: loss, D: draw, W: win}[ours][theirs]
    return shape_scores[our_shape] + outcome_scores[ours]

def p1() -> any:

    total_score = 0

    lines = get_input(2)
    
    for line in lines:
        their_move, our_move = line.strip().split(' ')
        score = outcome1(their_move, our_move)
        total_score += score

    return total_score

def p2() -> any:

    total_score = 0

    lines = get_input(2)
    
    for line in lines:
        their_move, our_move = line.strip().split(' ')
        score = outcome2(their_move, our_move)
        total_score += score

    return total_score


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
