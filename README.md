# Advent of Code - Python Solutions

## Setup

I'm assuming you've read the README on the main branch and have just forked and cloned this repo.
Here's the instructions again:

When you've got your own repo, make a virtual environment and install the `paoc` package:

```shell
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -e .
```

Now find your cookie for the Advent of Code website and export it as an environment variable:

```shell
export AOC_COOKIE="your-cookie-here"
```

Also export the year you want to work on as two digits (I don't think I'll be around for the 22$^{\mathrm{nd}}$ century):

```shell
export AOC_YEAR="23"
```

The `setup` command will now create a directory for the year you specified, which should look like this:

```shell
./paoc/y23
        ├── __init__.py    [just a basic docstring]
        ├── titles.txt     [empty file]
        ├── answers.txt    [empty file]
        ├── input          [0 files]
        └── solutions      [0 files]
```

## Usage

When you want to start for a new day, run the `scaffold` command with the day number as an argument:

```shell
scaffold 1
```

This will download the input for the day to _input/day1.txt_ and create a file for your solution in _solutions/day1.py_.

It will also add the title of the puzzle to _titles.txt_ (we use this for the docstring in the solution file) and for pretty printing the output.

Your solution file will be based off this [template](paoc/template.py) and should look something like this when parsed:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 23 Day 1 - Trebuchet?! """

from paoc.helper import get_input, print_summary


def p1() -> any:
    _ = get_input(1)

def p2() -> any:
    _ = get_input(1)


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
```

Naturally, `p1` and `p2` will return your solutions to part 1 and 2 respectively.

Now, you could run the file manually with `python3 paoc/y23/solutions/day1.py` but that's not very fun.

Instead, you can use the `solve` command to run it for you:

```shell
solve 1
```

This will run both parts of the solution and print the output to the terminal, along with some info on the execution time.

If `p2` doesn't return anything yet this will not break the code, it will just print `None` for part 2.

If you're a few days in, you can also run `solve all` to run all the solutions you've written so far.

For now, you will still have to manually copy the output to the AoC website to get your stars.
