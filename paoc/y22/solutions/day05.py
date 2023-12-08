#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 22 Day 5 - Supply Stacks """

from paoc.helper import get_input, print_summary


def extract_stacks(stack_part: list[str]) -> tuple[list[list[str]], int]:
    """ Takes the stack part of the input lines and returns a list of lists with single characters in them. """
    
    # last line of stack_input is not really all that useful
    n_stacks = int(stack_part[-1][-2])
    stack_part.pop()

    # integers representing on what index one stack ends, and the next one begins
    stack_seps: list[int] = [0] + list(range(3, 4*n_stacks, 4))

    # this is going to contain n_stacks lists of characters
    stacks: list[list[str]] = []

    for j, sep in enumerate(stack_seps[:-1]):
        next_sep = stack_seps[j+1]
        stack = list(reversed([
            line[sep:next_sep].strip().replace('[', '').replace(']', '')
            for line in stack_part
        ]))
        stack = [el for el in stack if el != '']
        stacks.append(stack)

    return stacks

def p1() -> any:
    lines = get_input(5)
    # first we extract the stack part of the input file (as a string)
    stack_part: list[str] = []
    line: str = lines[0]
    i: int = 1
    while line != '':
        stack_part.append(line)
        line = lines[i]
        i += 1

    stacks = extract_stacks(stack_part)

    for line in lines[i:]:
        _, n, _, from_stack, _, to_stack = line.split(' ')
        # cast to integers, and make from- and to-stack usable as indices
        n, from_stack, to_stack = int(n), int(from_stack)-1, int(to_stack)-1
        for _ in range(n):
            crate: list[str] = stacks[from_stack].pop()
            stacks[to_stack].append(crate)
    
    top_crates: str = ''.join([stack[-1] for stack in stacks])

    return top_crates

def p2() -> any:
    lines = get_input(5)
    # first we extract the stack part of the input file (as a string)
    stack_part: list[str] = []
    line: str = lines[0]
    i: int = 1
    while line != '':
        stack_part.append(line)
        line = lines[i]
        i += 1

    stacks = extract_stacks(stack_part)

    for line in lines[i:]:
        _, n, _, from_stack, _, to_stack = line.split(' ')
        # cast to integers, and make from- and to-stack usable as indices
        n, from_stack, to_stack = int(n), int(from_stack)-1, int(to_stack)-1
        crates: list[str] = stacks[from_stack][-n:]  # store the part to be moved
        for _ in range(n): stacks[from_stack].pop()  # we still need to pop in order to remove
        stacks[to_stack].extend(crates)
    
    top_crates: str = ''.join([stack[-1] for stack in stacks])

    return top_crates


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
