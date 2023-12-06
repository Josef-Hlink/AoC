#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" General helper functions; some public, some private. """

import os
from datetime import datetime
from timeit import Timer
from typing import Callable

from paoc.constants import YEAR, COOKIE, ROOT, INPUTS, PAOC, SOLUTIONS


##########
# PUBLIC #
##########

def get_input(day: int = None) -> list[str]:
    """ Return the input for a given day's puzzle as a list of strings.
    If no day is given, use today's date.
    If input file is not already downloaded, download it.
    """
    day = day or datetime.today().day
    if not INPUTS.exists():
        INPUTS.mkdir(parents=True)
    if not (INPUTS / f'day{day}.txt').exists():
        print(f'{_bold("WARNING")} input file for day {day} not found.')
        _download_input_file(day)
    with open(INPUTS / f'day{day}.txt', 'r') as f:
        lines = f.read().splitlines()
    return lines

def parse_multiline_string(multiline_string: str) -> list[str]:
    """ Allows you to paste the example input as a multiline string and have it be a list of strings.
    
    Example usage:
    ```
    from paoc.helper import parse_multiline_string as pms
    ex_lines = pms(\"\"\"
    hello
    world
    123
    \"\"\")
    ex_lines: list[str]  # ['hello', 'world', '123']
    ```
    """
    return multiline_string[1:].splitlines()

def print_summary(caller: str, p1: Callable[[], any], p2: Callable[[], any], n = 100) -> None:
    """ Print the summary for the day.
    ### args:
    `caller`: the `__file__` variable from the caller file.
    `p1`, `p2`: functions that return the solutions for part 1 and part 2 respectively.
    These solutions are printed, along with some insights on the performance.
    `n`: number of times functions are called in performance test.
    """
    day = int(caller.split('day')[1].split('.')[0])  # caller is /path/to/day[X]X.py
    print(f'day {day} - ' + _bold(_get_title(day)))
    print(_bold('solutions'))
    print(f'> 1: {p1()}')
    print(f'> 2: {p2()}')
    print(_bold('performance') + f' (ran {n} times)')
    print(f'> 1: {_fmt_runtime(Timer(p1).timeit(n)/n)} per run')
    print(f'> 2: {_fmt_runtime(Timer(p2).timeit(n)/n)} per run')
    return

#######
# CLI #
#######

def setup() -> None:
    """ Create directory structure for the year. """
    # inputs
    assert not INPUTS.exists(), f'inputs directory for year 20{YEAR} already exists'
    INPUTS.mkdir(parents=True)
    # solutions
    assert not SOLUTIONS.exists(), f'solutions directory for year 20{YEAR} already exists'
    SOLUTIONS.mkdir(parents=True)
    # __init__.py
    with open(PAOC / '__init__.py', 'w') as f:
        f.write(f'""" Everything related to the 20{YEAR} installment of Advent of Code. """\n')
    # titles.txt
    with open(PAOC / 'titles.txt', 'w') as f:
        f.write('')
    # answers.txt
    with open(PAOC / 'answers.txt', 'w') as f:
        f.write('')
    print(f'setup for 20{YEAR} complete, run `paoc scaffold <day>` to create a solution file')
    return

def scaffold(day: int) -> None:
    """ Create boilerplate .py file for a given day's puzzle. """
    assert day <= datetime.today().day, f'cannot scaffold for future days'
    title = _get_title(day)
    if not (INPUTS / f'day{day}.txt').exists():
        _download_input_file(day)    
    assert not (SOLUTIONS / f'day{day}.py').exists(), f'solution for day {day} already exists'
    with open(PAOC / f'template.py', 'r') as f:
        lines = f.read().splitlines()
    lines[3] = f'""" AoC {YEAR} Day {day} - {title} """'
    with open(SOLUTIONS / f'day{day}.py', 'w') as f:
        f.writelines('\n'.join(lines) + '\n')
    return

def solve(day: int) -> None:
    """ Run solution script for given day's puzzle. """
    assert (SOLUTIONS / f'day{day}.py').exists(), f"solution for day {day} doesn't exist"
    os.system(f'python {SOLUTIONS / f"day{day}.py"}')
    return

###########
# PRIVATE #
###########

def _get_title(day: int = None) -> str:
    """ Return the title for a given day's puzzle.
    If no day is given, use today's date.
    If the title is not found, print a warning and return an empty string.
    """
    day = day or datetime.today().day
    with open(PAOC / f'y{YEAR}' / 'titles.txt', 'r') as f:
        lines = f.read().splitlines()
    titles = {int(line.split(': ')[0]): line.split(': ')[1] for line in lines}
    if day not in titles:
        print(f'{_bold("WARNING")} title for day {day} not found.')
        _scrape_title(day)
        return _get_title(day)  # call function again to get the title
    return titles[day]

def _bold(text: str) -> str:
    return '\033[1m' + text + '\033[0m'

def _download_input_file(day: int) -> None:
    """ Use `curl` to download the input file for a given day's puzzle. """
    url = f'https://adventofcode.com/20{YEAR}/day/{day}/input'
    print(f'downloading input file from {url}')
    os.system(f'curl {url} -H "cookie: session={COOKIE}" > {INPUTS / f"day{day}.txt"}')
    return

def _scrape_title(day: int) -> None:
    """ Scrape the title for a given day's puzzle and add it to titles.txt. """
    url = f'https://adventofcode.com/20{YEAR}/day/{day}'
    print(f'scraping title from {url}')
    os.system(f'curl {url} -H "cookie: session={COOKIE}" > {ROOT / "tmp.html"}')
    with open(ROOT / 'tmp.html', 'r') as f:
        html = f.read().splitlines()
    line = [line for line in html if line.startswith('<article class="day-desc"><h2>')][0]
    os.system(f'rm {ROOT / "tmp.html"}')
    assert str(day) in line, f'could not find title for day {day}'
    title = line.split('---')[1].split(': ')[1][:-1]
    with open(PAOC / f'y{YEAR}' / 'titles.txt', 'a') as f:
        f.write(f'{day}: {title}\n')
    return

def _fmt_runtime(seconds: float) -> str:
    """ Format runtime given in ms, s, or m:ss """
    if seconds < 1:
        return f'{seconds*1000:.2f} ms'
    if 1 < seconds < 60:
        return f'{seconds:.2f} s'
    if seconds >= 60:
        return f'{seconds//60}:{int(seconds%60):02}'
