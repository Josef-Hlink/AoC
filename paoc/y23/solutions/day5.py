#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 23 Day 5 - If You Give A Seed A Fertilizer """

from paoc.helper import get_input, print_summary
from itertools import groupby


class Plant:
    """ Contains data of what ranges of seeds, soils, etc. a plant has. """
    def __init__(self, seed: int | set[range]):
        self.seed = seed
        self.dtype = type(seed)
        
    def __str__(self) -> str:
        items = filter(lambda x: x[0] != 'dtype', self.__dict__.items())
        if self.dtype == int:
            return f'\n'.join([f'{" " * i}> {k[:2]}: {v}' for i, (k, v) in enumerate(items)])
        else:
            return f'\n'.join([f'{" " * i}> {k[:2]}: {" | ".join([f"{x.start}-{x.stop}" for x in v])}' for i, (k, v) in enumerate(items)])

class Rule:
    """ A rule that maps a range of values to another range. """
    def __init__(self, line: str):
        """ `line` has the form "dst_start src_start map_length". """
        d, s, l = map(lambda x: int(x), line.split())
        self.funnel = range(s, s+l)
        self.offset = d - s
    
    def apply(self, x: int | range) -> int | range:
        """ Applies a rule to a number or a range of numbers.
        If `x` is a single number, simply returns its value mapped by `self.offset` (we checked that it's in funnel earlier).
        If `x` is a range, returns the intersection of `x` and `self.funnel` mapped by `self.offset` (could be an empty range).
        """
        if type(x) == int: return x + self.offset
        else: return range(max(x.start, self.funnel.start) + self.offset, min(x.stop, self.funnel.stop) + self.offset)
        
    def __str__(self) -> str:
        return fr'\{self.funnel.start}-{self.funnel.stop-1}/ -> {"+" if self.offset>0 else ""}{self.offset}'

class Mapper:
    """ Handles all rules for mapping seed numbers to soil numbers, soil numbers to fertilizer numbers, etc. """
    def __init__(self, lines: list[str]):
        """ `lines[0]` contains metadata, `lines[1:]` contain the rules.  """
        self.src, self.dst = lines[0].removesuffix(' map:').split('-to-')
        self.rules = list(sorted([Rule(line) for line in lines[1:]], key=lambda x: x.funnel.start))
        self._handle_missing_rules()
    
    def _handle_missing_rules(self) -> None:
        """ Not all value ranges are described in the input mappings, but we do need them. """
        # head
        if (lowest_start := self.rules[0].funnel.start):
            self.rules.insert(0, Rule(f'0 0 {lowest_start}'))
        # tail
        ridiculously_high_number = (highest_stop := self.rules[-1].funnel.stop) * 100
        self.rules.append(Rule(f'{highest_stop} {highest_stop} {ridiculously_high_number}'))
        # gaps
        gaps = []
        for i, rule in enumerate(self.rules[1:], start=1):
            if (curr_start := rule.funnel.start) != (prev_stop := self.rules[i-1].funnel.stop):
                gaps.append(Rule(f'{prev_stop} {prev_stop} {curr_start-prev_stop}'))
        self.rules = list(sorted(self.rules + gaps, key=lambda x: x.funnel.start))

    def apply(self, x: int | set[range]) -> int | set[range]:
        """ Applies all the rules to the ranges. """
        # find out which rule we need and apply it
        if type(x) == int: return list(filter(lambda rule: x in rule.funnel, self.rules))[0].apply(x)
        # apply all rules to all ranges, checking would be more performant but way uglier
        else: return {rule.apply(_x) for rule in self.rules for _x in x}

    def __str__(self) -> str:
        return f'{self.src} to {self.dst}:\n' + '\n'.join([str(rule) for rule in self.rules])

def p1() -> any:
    almanac = get_input(5)
    plants = list(map(lambda x: Plant(int(x)), almanac[0].split(': ')[1].split()))
    mappers = [Mapper(list(g)) for k, g in groupby(almanac[2:], lambda x: x == '') if not k]

    for plant in plants:
        for mapper in mappers:
            x = plant.__getattribute__(mapper.src)
            y = mapper.apply(x)
            plant.__setattr__(mapper.dst, y)

    return min([p.location for p in plants])

def p2() -> any:
    almanac = get_input(5)
    plants = [Plant([range(int(x), int(x) + int(y))]) for x, y in zip(*[iter(almanac[0].split(': ')[1].split())]*2)]
    mappers = [Mapper(list(g)) for k, g in groupby(almanac[2:], lambda x: x == '') if not k]

    for plant in plants:
        for mapper in mappers:
            x = plant.__getattribute__(mapper.src)
            y = mapper.apply(x)
            plant.__setattr__(mapper.dst, y)

    return min([min([r.start for r in p.location]) for p in plants])


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
