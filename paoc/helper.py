# -*- coding: utf-8 -*-

"""General helper functions; some public, some private."""

import os
import re
from collections.abc import Callable
from datetime import datetime
from timeit import Timer
from typing import Optional, cast

from bs4 import BeautifulSoup, Tag

from paoc.constants import COOKIE, INPUTS, PAOC, ROOT, SOLUTIONS, YEAR

##########
# PUBLIC #
##########


def get_input(day: Optional[int] = None, example: bool = False) -> list[str]:
    """Return the input for a given day's puzzle as a list of strings.

    If no day is given, use today's date.
    If input file is not already downloaded, download it.
    If `example` is True, return the example input instead.
    """
    day = day or datetime.today().day
    zday = str(day).zfill(2)
    if not example and not (INPUTS / f'day{zday}.txt').exists():
        print(f'{_bold("WARNING")} input file for day {day} not found.')
        _download_input_file(day)
    if example and not (INPUTS / f'ex{zday}.txt').exists():
        print(f'{_bold("WARNING")} example input file for day {day} not found.')
        _scrape_example(day)
    prefix = 'ex' if example else 'day'
    with open(INPUTS / f'{prefix}{zday}.txt') as f:
        lines = f.read().splitlines()
    return lines


def parse_multiline_string(multiline_string: str) -> list[str]:
    """Allows you to paste the example input as a multiline string and have it be a list of strings.

    This is useful for testing with example inputs in the code itself, especially in notebooks.

    Example usage:

    ```python
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


def print_summary(caller: str, p1: Callable[[], int], p2: Callable[[], int], n: int = 100) -> None:
    """Print the summary for the day including title, solutions, and performance.

    Args:
        caller: the `__file__` variable from the caller file.
        p1: function that returns the solution for part 1.
        p2: function that returns the solution for part 2.
        n: number of times functions are called in performance test.
    """
    day = int(caller.split('day')[1].split('.')[0])  # caller is .../path/to/dayXX.py
    print(f'day {day} - ' + _bold(_get_title(day)))
    print(_bold('solutions'))
    print(f'> 1: {p1()}')
    print(f'> 2: {p2()}')
    print(_bold('performance') + f' (ran {n} times)')
    print(f'> 1: {_fmt_runtime(Timer(p1).timeit(n) / n)} per run')
    print(f'> 2: {_fmt_runtime(Timer(p2).timeit(n) / n)} per run')
    return


#######
# CLI #
#######


def setup() -> None:
    """Create directory structure for the year."""
    # inputs
    assert not INPUTS.exists(), f'inputs directory for year 20{YEAR} already exists'
    INPUTS.mkdir(parents=True)
    # solutions
    assert not SOLUTIONS.exists(), f'solutions directory for year 20{YEAR} already exists'
    SOLUTIONS.mkdir(parents=True)
    # __init__.py
    with open(PAOC / f'y{YEAR}' / '__init__.py', 'w') as f:
        f.write(f'"""Everything related to the 20{YEAR} installment of Advent of Code."""\n')
    # titles.txt
    with open(PAOC / f'y{YEAR}' / 'titles.txt', 'w') as f:
        f.write('')
    # answers.txt
    with open(PAOC / f'y{YEAR}' / 'answers.txt', 'w') as f:
        f.write('')
    print(f'setup for 20{YEAR} complete, run `scaffold <day>` to create a solution file')
    return


def scaffold(day: int) -> None:
    """Create boilerplate .py file for a given day's puzzle."""
    if 2000 + YEAR == datetime.today().year:
        assert day <= datetime.today().day, 'cannot scaffold for future days'
    title = _get_title(day)
    zday = str(day).zfill(2)
    if not (INPUTS / f'day{zday}.txt').exists():
        _download_input_file(day)
    if not (INPUTS / f'ex{zday}.txt').exists():
        _scrape_example(day)
    assert not (SOLUTIONS / f'day{zday}.py').exists(), f'solution for day {day} already exists'
    with open(PAOC / 'template.py') as f:
        lines = f.read().splitlines()
    replacements = {
        '<YY>': str(YEAR),
        '<DD>': str(day),
        '<Title>': title,
        '...': f'_ = get_input({day})',
    }
    new_lines = []
    for line in lines:
        for temp, new in replacements.items():
            line = line.replace(temp, new)
        new_lines.append(line)
    with open(SOLUTIONS / f'day{zday}.py', 'w') as f:
        f.writelines('\n'.join(new_lines) + '\n')
    return


def solve(day: int) -> None:
    """Run solution script for given day's puzzle."""
    zday = str(day).zfill(2)
    assert (SOLUTIONS / f'day{zday}.py').exists(), f"solution for day {day} doesn't exist"
    os.system(f'python3 {SOLUTIONS / f"day{zday}.py"}')
    return


###########
# PRIVATE #
###########


def _get_title(day: Optional[int] = None) -> str:
    """Return the title for a given day's puzzle.

    If no day is given, use today's date.
    """
    day = day or datetime.today().day
    with open(PAOC / f'y{YEAR}' / 'titles.txt') as f:
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
    """Use `curl` to download the input file for a given day's puzzle."""
    url = f'https://adventofcode.com/20{YEAR}/day/{day}/input'
    print(f'downloading input file from {url}')
    zday = str(day).zfill(2)
    os.system(f'curl {url} -H "cookie: session={COOKIE}" > {INPUTS / f"day{zday}.txt"}')
    return


def _scrape_title(day: int) -> None:
    """Scrape the title for a given day's puzzle and add it to titles.txt."""
    url = f'https://adventofcode.com/20{YEAR}/day/{day}'
    print(f'scraping title from {url}')
    os.system(f'curl {url} -H "cookie: session={COOKIE}" > {ROOT / "tmp.html"}')
    with open(ROOT / 'tmp.html') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    try:
        article = cast(Tag, soup.find('article', class_='day-desc'))
        h2 = cast(Tag, article.find('h2')).get_text()
        title = cast(re.Match, re.search(r'\d+:(.*?)---', h2)).group(1).strip()
    except Exception:
        title = 'N/A'
    os.system(f'rm {ROOT / "tmp.html"}')
    print(f'title for day {day}: {title}')
    with open(PAOC / f'y{YEAR}' / 'titles.txt', 'a') as f:
        f.write(f'{day}: {title}\n')
    return


def _scrape_example(day: int) -> None:
    """Scrape the first code block from a given day's puzzle and save it under inputs/exXX.txt."""
    url = f'https://adventofcode.com/20{YEAR}/day/{day}'
    print(f'scraping example from {url}')
    os.system(f'curl {url} -H "cookie: session={COOKIE}" > {ROOT / "tmp.html"}')
    with open(ROOT / 'tmp.html') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    try:
        article = cast(Tag, soup.find('article', class_='day-desc'))
        example = cast(Tag, article.find('pre')).get_text()
    except Exception:
        example = 'N/A'
    os.system(f'rm {ROOT / "tmp.html"}')
    print(f'example input for day {day}:\n{example}')
    with open(INPUTS / f'ex{str(day).zfill(2)}.txt', 'w') as f:
        f.write(example)
    return


def _fmt_runtime(seconds: float) -> str:
    """Format runtime given in ms, s, or m:ss."""
    assert seconds >= 0, 'seconds must be non-negative'
    if seconds < 1:
        return f'{seconds * 1000:.2f} ms'
    if 1 < seconds < 60:
        return f'{seconds:.2f} s'
    return f'{int(seconds // 60)}:{int(seconds % 60):02}'  # over one minute
