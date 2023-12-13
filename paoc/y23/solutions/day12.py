#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 23 Day 12 - Hot Springs """

from paoc.helper import get_input, print_summary
import re
from functools import cache


""" NOTE
I'm calling the DP approach for both parts in the `if __name__ == '__main__'` block here,
because it's way faster than the simple recursive one.
For more info on why the recursive function is still here, please see day 12 entry in my log.
"""

def count_total_arrangements(spring_records: list[str], approach: str, unfold: bool = False) -> int:
    """ Loop over the records & apply either the recursive or DP approach on each record. """
    
    assert approach in ['rec', 'dp'], \
        f'Invalid approach: {approach}, only "rec" and "dp" are implemented.'
    
    total = 0
    for record in spring_records:
        springs, groups = record.split()
        groups = tuple(map(int, groups.split(',')))
        if unfold:
            # make both springs and groups 5 times as big
            springs, groups = '?'.join([springs] * 5), groups * 5
        if approach == 'rec':
            total += count_arrangements_rec(template=springs, groups=groups)
        else:
            total += count_arrangements_dp(springs=springs, groups=groups)
    return total

def count_arrangements_rec(template: str, groups: tuple[int], springs: str = '') -> int:
    """ Count number of arrangements `template` can be in to match the `groups` signature
    using relatively intuitive recursion.
    ### args:
    - `template`: springs template containing question marks, e.g. `'.??..??...?##.'` (CONST).
    - `groups`: target signature of `'#'`-block lengths, e.g. `(1, 1, 3)` (CONST).
    - `springs`: current arrangement of springs we're constructing, e.g., `'.#..` (MUT).
    Note that the length of this string is always equal to recursion depth (starting at 0).
    """
    # --- BASE CASES ---
    if len(springs) == len(template):
        # we're at the end of template, so we check for equality of signatures
        return get_groups(springs) == groups
    else:
        # stop early if the groups signature already doesn't align with target
        if springs != '' and springs[-1] == '.':
            curr_groups = get_groups(springs)
            if curr_groups and curr_groups != groups[:len(curr_groups)]:
                return 0
    # --- REC CASES ---
    count = 0
    if template[len(springs)] == '?':
        count += count_arrangements_rec(template, groups, springs + '.')
        count += count_arrangements_rec(template, groups, springs + '#')
    else:
        count += count_arrangements_rec(template, groups, springs + template[len(springs)])
    return count

@cache
def get_groups(springs: str) -> tuple[int]:
    """ Helper function used in the basic recursive approach. """
    return tuple(group.end()-group.start() for group in re.finditer('#+', springs))

@cache
def count_arrangements_dp(springs: str, groups: tuple[int]) -> int:
    """ Count number of arrangements `template` can be in to match the `groups` signature
    using very abstract and hard-to-reason-about dynamic programming approach.
    ### args:
    - `springs`: string of springs left to process, e.g. `'.??...?##.'` (MUT).
    This string will be pruned f.l.t.r, i.e. `'.??...?##.'` -> `'??...?##.'`.
    - `groups`: target signature of `'#'`-block lengths, e.g. `(1, 3)` (MUT).
    This will also be pruned f.l.t.r if a correctly-sized group was found in `springs`.
    """
    # --- BASE CASES ---
    if not springs:
        # we've processed the entire arrangement of springs, so groups should also be empty
        return groups == ()
    if not groups:
        # there's no groups left to fit, so if there's a '#' left we discard this arrangement
        return '#' not in springs
    # --- REC CASES ---
    count = 0
    if springs[0] in '.?':
        # nothing happens, just move on to the next spring
        count += count_arrangements_dp(springs[1:], groups)
    if springs[0] in '#?':
        # there's three conditions that have to be met if we want to recurse further
        if groups[0] <= len(springs):  # enough springs left
            if '.' not in springs[:groups[0]]:  # next N springs are (or could be) broken
                if groups[0] == len(springs) or springs[groups[0]] in '.?':  # group ends
                    count += count_arrangements_dp(springs[groups[0]+1:], groups[1:])
    return count
    

def p1() -> int:
    return count_total_arrangements(spring_records=get_input(12), approach='dp')

def p2() -> int:
    return count_total_arrangements(spring_records=get_input(12), approach='dp', unfold=True)


if __name__ == '__main__':
    print_summary(__file__, p1, p2, n=100)
