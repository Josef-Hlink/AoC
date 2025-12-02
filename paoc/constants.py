# -*- coding: utf-8 -*-

"""Constants for paoc."""

import os
from pathlib import Path

# environment variables
YEAR: int = int(os.environ['AOC_YEAR'])
COOKIE: str = os.environ['AOC_COOKIE']

# paths
ROOT = Path(__file__).parent.parent
PAOC = ROOT / 'paoc'
INPUTS = PAOC / f'y{YEAR}' / 'inputs'
SOLUTIONS = PAOC / f'y{YEAR}' / 'solutions'
