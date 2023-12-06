#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 22 Day 11 - Monkey in the Middle """

from paoc.helper import get_input, print_summary
from typing import Callable


class Monkey:
    def __init__(
            self,
            packages: list[int],
            operation: Callable[[int], int],
            divisor: int,
            pass_to: tuple[int, int]
        ):
        self.packages = packages
        self.operation = operation
        self.pass_to = pass_to
        self.divisor = divisor
        self.packages_handled = 0
    
    def handle_package1(self) -> tuple[int, int]:
        """ Monkey will handle the first package in its list (operation and passing) """
        package: int = self.packages.pop(0)
        package = self.operation(package)
        package = package//3
        next_monkey = self.pass_to[package%self.divisor==0]
        self.packages_handled += 1
        return next_monkey, package

    def handle_package2(self, mod) -> tuple[int, int]:
        """ Monkey will handle the first package in its list (operation and passing) """
        package: int = self.packages.pop(0)
        package = self.operation(package)
        package = package % mod
        next_monkey = self.pass_to[package%self.divisor==0]
        self.packages_handled += 1
        return next_monkey, package

def sanitize_input(
        lines: list[str]
    )-> tuple[list[int], Callable[[int], int], int, tuple[int, int]]:
    """ Extracts all attributes of a monkey from a chunk of input lines """
    starting_packages = [int(n) for n in lines[1].split(': ')[1].split(', ')]
    operation = op_str_to_lambda(expression=lines[2].split(' = ')[1])
    divisor = int(lines[3].split(' ')[-1])
    pass_to = (int(lines[5].split(' ')[-1]), int(lines[4].split(' ')[-1]))  # 0=F, 1=T
    return starting_packages, operation, divisor, pass_to

def op_str_to_lambda(expression: str) -> Callable[[int], int]:
    # a is always "old", so will be called x in our lambda function
    _, operator, b = expression.split(' ')
    if b != 'old':  # b is an integer
        return (lambda x: x + int(b)) if operator == '+' else (lambda x: x * int(b))
    else:  # b is x
        return (lambda x: x + x) if operator == '+' else (lambda x: x * x)

def p1() -> any:
    
    lines = get_input(11)
    # remove empty lines
    lines = list(filter(lambda line: line != '', lines))

    # instantiate monkey objects
    monkeys: list[Monkey] = []
    for i in range(0, len(lines), 6):
        starting_packages, operation, divisor, pass_to = sanitize_input(lines[i:i+6])
        monkeys.append(Monkey(starting_packages, operation, divisor, pass_to))
    
    # play 20 rounds
    for _ in range(20):
        for monkey in monkeys:
            while len(monkey.packages) > 0:
                next_monkey, package = monkey.handle_package1()
                monkeys[next_monkey].packages.append(package)
    
    # see how active they have been
    activities: list[int] = sorted([m.packages_handled for m in monkeys], reverse=True)
    return activities[0] * activities[1]


def p2() -> any:

    lines = get_input(11)
    # remove empty lines
    lines = list(filter(lambda line: line != '', lines))

    # instantiate monkey objects
    monkeys: list[Monkey] = []
    for i in range(0, len(lines), 6):
        starting_packages, operation, divisor, pass_to = sanitize_input(lines[i:i+6])
        monkeys.append(Monkey(starting_packages, operation, divisor, pass_to))
    
    # define a number we can safely "mod" all the worry levels by
    mod = 1
    for div in [m.divisor for m in monkeys]: mod *= div

    # play 10000 rounds
    for _ in range(10000):
        for monkey in monkeys:
            while len(monkey.packages) > 0:
                next_monkey, package = monkey.handle_package2(mod)
                monkeys[next_monkey].packages.append(package)
    
    # see how active they have been
    activities: list[int] = list(sorted([m.packages_handled for m in monkeys], reverse=True))
    return activities[0] * activities[1]


if __name__ == '__main__':
    print_summary(__file__, p1, p2, n=10)
