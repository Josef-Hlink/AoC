#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 24 Day 9 - Disk Fragmenter """

from paoc.helper import get_input, print_summary


def init_disk(disk_map: str) -> tuple[list[str], list[int], list[int]]:
    disk = []
    files = list(map(int, disk_map[::2]))
    gaps = list(map(int, disk_map[1::2])) + [0]
    for i in range(len(files)):
        disk += [str(i)] * files[i]
        disk += ['.'] * gaps[i]
    return disk, files, gaps

def check(disk: list[int]) -> int:
    return sum(map(lambda i: i * int(disk[i]) if disk[i] != '.' else 0, range(len(disk))))


def p1() -> any:
    disk, _, _ = init_disk(get_input(9)[0])
    while '.' in disk:
        disk[disk.index('.')] = disk.pop()
    return check(disk)

def p2() -> any:
    disk, files, gaps = init_disk(get_input(9)[0])
    for i in range(len(files)-1, -1, -1):
        nb = files[i]  # nb = num blocks, gs = gap size
        j = next((j_ for j_, gs in enumerate(gaps) if gs >= nb), None)
        if j is not None and j < i:
            # wipe at orig pos
            y = disk.index(str(i))
            disk[y:y+nb] = ['.'] * nb
            # insert in gap
            x = (t:=disk.index(str(j))) + disk[t:].index('.')
            disk[x:x+nb] = [i] * nb
            # update gaps register
            gaps[j] -= nb
    return check(disk)


if __name__ == '__main__':
    print_summary(__file__, p1, p2, n=1)
