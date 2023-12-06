#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Command line interface methods for paoc. """

import sys
from paoc.constants import SOLUTIONS
from paoc.helper import scaffold, solve


def scaffold_cli() -> None:
    """ Create boilerplate .py file for a given day's puzzle. """
    assert len(sys.argv) == 2, f'usage: scaffold <day>'
    day = int(sys.argv[1])
    scaffold(day)
    return

def solve_cli() -> None:
    """ Run solution script for given day's puzzle. """
    assert len(sys.argv) == 2, f'usage: solve <day>|all'
    if sys.argv[1] == 'all':
        for file in sorted(SOLUTIONS.iterdir()):
            if not file.name.startswith('day'): continue
            solve(int(file.stem.removeprefix('day')))
            print('-' * 64)
    else:
        day = int(sys.argv[1])
        solve(day)
    return
