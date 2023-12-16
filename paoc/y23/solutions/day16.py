#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 23 Day 16 - The Floor Will Be Lava """

from paoc.helper import get_input, print_summary


N = (-1, 0)
S = (+1, 0)
W = (0, -1)
E = (0, +1)

class Photon:
    def __init__(self, pos: tuple[int, int], dir: tuple[int, int]):
        self.pos = pos
        self.dir = dir

    def move(self) -> None:
        next_pos = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])
        self.pos = next_pos

def find_energized(contraption: list[str], origin: Photon) -> set[tuple[int, int]]:

    nr, nc = len(contraption), len(contraption[0])

    mirrors = {
        '/':  {N: E,  S: W,  W: S,  E: N},
        '\\': {N: W,  S: E,  W: N,  E: S}
    }
    splits = {
        '-': {N: (W, E),  S: (W, E)},
        '|': {W: (N, S),  E: (N, S)}
    }

    photons = [origin]
    sources = {(origin.pos, origin.dir)}

    energized: set[tuple[int, int]] = set()
    while photons:
        for p in photons:
            while -1 < p.pos[0] < nr and -1 < p.pos[1] < nc:
                energized.add(p.pos)
                tile_type = contraption[p.pos[0]][p.pos[1]]
                if tile_type == '.':
                    # this happens often, so we save time by skipping slightly more expensive checks
                    pass
                elif tile_type in mirrors:
                    # direction just gets changed, but we'll keep using the same photon object
                    p.dir = mirrors[tile_type][p.dir]
                elif tile_type in splits and p.dir in splits[tile_type]:
                    # two new photon objects are created (if we haven't seen them before)
                    new_dirs = splits[tile_type][p.dir]
                    for p_ in (Photon(p.pos, new_dirs[0]), Photon(p.pos, new_dirs[1])):
                        if (p_.pos, p_.dir) not in sources:
                            photons.append(p_)
                            sources.add((p_.pos, p_.dir))
                    # the old photon dies
                    break
                p.move()
            photons.remove(p)
    return energized


def p1() -> int:
    return len(find_energized(get_input(16), Photon((0, 0), E)))

def p2() -> int:
    contraption = get_input(16)
    nr, nc = len(contraption), len(contraption[0])
    max_energized = 0
    for r in range(nr):
        max_energized = max(max_energized, len(find_energized(contraption, Photon((r, 0), E))))
        max_energized = max(max_energized, len(find_energized(contraption, Photon((r, nc-1), W))))
    for c in range(nr):
        max_energized = max(max_energized, len(find_energized(contraption, Photon((0, c), S))))
        max_energized = max(max_energized, len(find_energized(contraption, Photon((nr-1, c), N))))
    return max_energized


if __name__ == '__main__':
    print_summary(__file__, p1, p2, n=10)
