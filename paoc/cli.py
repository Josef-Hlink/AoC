# -*- coding: utf-8 -*-

"""Command line interface methods for paoc."""

import sys

from paoc.constants import SOLUTIONS
from paoc.helper import scaffold, setup, solve


def setup_cli() -> None:
    """Create directory structure for the year."""
    setup()
    return


def scaffold_cli() -> None:
    """Create boilerplate .py file for a given day's puzzle."""
    assert len(sys.argv) == 2, 'usage: scaffold <day>'
    day = int(sys.argv[1])
    scaffold(day)
    return


def solve_cli() -> None:
    """Run solution script for given day's puzzle."""
    assert len(sys.argv) == 2, 'usage: solve <day>|all'
    if sys.argv[1] == 'all':
        for file in sorted(SOLUTIONS.iterdir()):
            if not file.name.startswith('day'):
                continue
            solve(int(file.stem.removeprefix('day')))
            print('-' * 64)
    else:
        day = int(sys.argv[1])
        solve(day)
    return
