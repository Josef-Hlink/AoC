#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 23 Day 10 - Pipe Maze """

from paoc.helper import get_input, print_summary
import sys


# global variables related to directions
U, D, L, R = (-1, 0), (+1, 0), (0, -1), (0, +1)  # up down left right
DIRS: dict[str, set[tuple[int, int]]] = {
    '|': {U, D},
    '-': {L, R},
    'L': {U, R},
    'J': {U, L},
    '7': {D, L},
    'F': {D, R},
    '.': {},
    'S': {U, D, L, R}
}

# for easier debugging
PRETTY_CHARS = {
    '|': '\u2502',  # │
    '-': '\u2500',  # ─
    'L': '\u2514',  # └
    'J': '\u2518',  # ┘
    '7': '\u2510',  # ┐
    'F': '\u250C',  # ┌
    '.': '.',
    'S': 'S'
}

class Pipe:
    def __init__(self, char: str, r: int, c: int, in_dir: tuple[int, int] | None = None):
        """ Create a pipe object.
        ### args:
        - `char`: one of `"|-LJ7FS."`.
        - `r`: row in grid.
        - `c`: column in grid.
        - `in_dir`: direction from which the pipe is entered (relative to `S`).
        Starting pipe `S` does not have this property (yet)
        """
        self.char = char
        self.pchar = PRETTY_CHARS[char]
        self.r, self.c = r, c
        self.pos = (self.r, self.c)  # allows for nicer API when taking steps
        self.in_dir = in_dir
        self.dirs = DIRS[self.char]
        if self.char != 'S':
            in_dir_flipped = (-self.in_dir[0], -self.in_dir[1])
            self.next_dir = (self.dirs - {in_dir_flipped}).pop()
    
    @property
    def r_sign(self) -> int:
        """ Row sign; -1 if we're going up, +1 if we're going down, and 0 if we're moving strictly sideways. """
        return self.next_dir[0] if self.next_dir[0] != 0 else self.in_dir[0]
    
    def is_connected_to(self, other: "Pipe") -> bool:
        """ Returns whether or not a pipe is connected to another pipe. """
        assert abs(self.r-other.r + self.c-other.c) == 1, f'Pipes {self} & {other} are not neighbors'
        if other.r == self.r - 1: return U in self.dirs and D in other.dirs  # other is up
        if other.r == self.r + 1: return D in self.dirs and U in other.dirs  # other is down
        if other.c == self.c - 1: return L in self.dirs and R in other.dirs  # other is left
        if other.c == self.c + 1: return R in self.dirs and L in other.dirs  # other is right

    def __matmul__(self, other: "Pipe") -> bool:
        """ Overloads the `@` operator for more aesthetically pleasing API. """
        return self.is_connected_to(other)
    
    def __str__(self) -> str:
        return f'[ {self.pos} \033[40m{[self.pchar]}\033[49m ]'


class Pipeline:
    def __init__(self, pipes: list[Pipe] = None):
        self.pipes = pipes or []
    
    def add(self, pipe: Pipe) -> None:
        self.pipes.append(pipe)
        return

    def complete_loop(self) -> None:
        """ Complete the loop by adding the correct `in_dir` & `next_dir` attributes for our starting pipe. """
        self.pipes[0].next_dir = self.pipes[1].in_dir
        self.pipes[0].in_dir = self.pipes[-1].next_dir
        return

    def get_pipes_in_row(self, r: int) -> list[Pipe]:
        """ Return all the pipe objects present in row `r` of the grid, sorted by column. """
        return list(sorted([p for p in self.pipes if p.r == r], key=lambda p: p.c))
    
    def __len__(self) -> int:
        return len(self.pipes)


def step(pos: tuple[int, int], dydx: tuple[int, int]) -> tuple[int, int]:
    """ Utility function because tuples don't support item-wise addition. """
    return (pos[0] + dydx[0], pos[1] + dydx[1])

def find_pipeline(grid: list[str]) -> Pipeline:
    """ Create a pipeline object from the input file. """
    
    # find starting position
    for r, row in enumerate(grid):
        c = row.find('S')
        if c != -1:
            break
    start = Pipe('S', r, c)

    # python doesn't have dowhile-loops, so we have to resort to some ugly syntax
    pipeline = Pipeline()
    pipeline_found = False
    for start_dir in start.dirs:
        # break out of this for-loop if we've already found the pipe loop
        if pipeline_found:
            break
        # take a step
        r, c = step(start.pos, start_dir)
        pipe = Pipe(grid[r][c], r, c, in_dir=start_dir)
        if not start @ pipe:  # pipes are not connected, so we
            continue          # skip this path
        # store starting pipe and its first neighbor
        pipeline = Pipeline([start, pipe])
        # walk until we find the starting pipe again
        while pipe.char != 'S':
            r, c = step(pipe.pos, pipe.next_dir)
            next_pipe = Pipe(grid[r][c], r, c, in_dir=pipe.next_dir)
            if not pipe @ next_pipe:  # pipes are not connected, so we
                break                 # stop exploring this path
            pipeline.add(pipe)
            pipe = next_pipe
        else:                      # while-loop was not broken out of,
            pipeline_found = True  # meaning we found the loop!
    
    # set direction for starting pipe, because we didn't know it at the start
    pipeline.complete_loop()

    return pipeline

def next_pipe_in_row(pipes: list[Pipe], r_sign: int = None) -> Pipe | None:
    """ Returns the next pipe with the `r_sign` opposite to the one provided.
    If no `r_sign` is provided, simply returns the first pipe with a non-zero one.
    NOTE: this function modifies the pipes list!
    """
    targets = {-1, 1} if r_sign is None else {-r_sign}
    while r_sign not in targets:
        if not pipes:
            return None
        pipe = pipes.pop(0)
        r_sign = pipe.r_sign
    return pipe

def find_area(grid: list[str], pipeline: Pipeline) -> list[tuple[int, int]]:
    """ Find the area enclosed in the pipeline loop using the non-zero winding rule. """
    area = []
    for r, row in enumerate(grid):
        pipes = pipeline.get_pipes_in_row(r)
        # column numbers with pipes that are part of the pipeline
        pipe_positions = set(p.c for p in pipes)
        # will be flipped on and off for each span
        inside = False
        c, r_sign = 0, None
        while c < len(row):
            pipe = next_pipe_in_row(pipes, r_sign)
            if not pipe:
                break
            if inside:
                # these are all positions enclosed in the loop
                span = range(c+1, pipe.c)
                # but we need to subtract the positions that are part of the loop themselves
                area.extend((r, c_) for c_ in (set(span) - pipe_positions))
            c, r_sign = pipe.c, pipe.r_sign
            inside = not inside
    return area

def visualize() -> None:
    """ Print the grid with the pipeline loop. """
    grid = get_input(10)
    pipeline = find_pipeline(grid)
    area = find_area(grid, pipeline)
    for r, row in enumerate(grid):
        pipes = pipeline.get_pipes_in_row(r)
        print(f'{r:3d} ', end='')
        for c, char in enumerate(row):
            if pipes and pipes[0].c == c:
                print('\033[40m' + pipes.pop(0).pchar + '\033[49m', end='')
            elif (r, c) in area:
                print('\033[42m' + PRETTY_CHARS[char] + '\033[49m', end='')
            else:
                print('\033[41m' + PRETTY_CHARS[char] + '\033[49m', end='')
        print()
    return

def p1() -> int:
    grid = get_input(10)
    pipeline = find_pipeline(grid)
    return len(pipeline)//2

def p2() -> int:
    grid = get_input(10)
    pipeline = find_pipeline(grid)
    area = find_area(grid, pipeline)
    return len(area)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'visualize':
        visualize()
    else:
        print_summary(__file__, p1, p2, n=10)
