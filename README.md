# Advent of Code - Python Solutions

This repository contains my solutions to the [Advent of Code](https://adventofcode.com/) puzzles, written in Python.
Solutions for different years will live in different directories:
- _paoc/y22/solutions/day1.py_
- _paoc/y23/solutions/day2.py_
- etc.

Having one repository is just something I like.

```
.
├── README.md
├── pyproject.toml
├── LICENSE
└── paoc
    ├── __init__.py
    ├── cli.py
    ├── constants.py
    ├── helper.py
    ├── play.ipynb
    ├── template.py
    └── y23
        ├── __init__.py
        ├── inputs
        │   ├── day1.txt
        │   └── ...
        ├── solutions
        │   ├── __init__.py
        │   ├── day1.py
        │   └── ...
        ├── answers.txt
        └── titles.txt
```

## Setup

If you also want to participate in the Advent of Code, you could just #yolo it by creating loose _.py_ files and running them manually.
However, I've created this repository so everything is nice and neat, while still being able to focus on the puzzles themselves.
If you're looking for a similar setup, here's how to get started.

First, fork the [template branch](https://github.com/Josef-Hlink/AoC/tree/template) of this repository and clone it to your local machine.

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

## Usage

TODO
