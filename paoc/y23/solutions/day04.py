#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 23 Day 4 - Scratchcards """

from paoc.helper import get_input, print_summary
import re
from collections import defaultdict


def parse_card(card: str) -> tuple[int, set[int], set[int]]:
    """ Extracts `card_id`, `winning_numbers`, `my_numbers` for a card. """
    card_id = int(re.match(r'Card\s+(\d+):', card).group(1))
    winning_numbers, my_numbers = map(lambda numbers: set(re.findall(r'\d+', numbers)), card.split(':')[1].split('|'))
    return card_id, winning_numbers, my_numbers

def p1() -> any:
    """ Sum of points won on all cards in the pile. """
    return sum([int(2**(len(w.intersection(m))-1)) for _, w, m in map(parse_card, get_input(4))])

def p2() -> any:
    """ Total number of card copies we have after scratching the cards. """
    copies = defaultdict(int)
    for card in get_input(4):
        card_id, winning_numbers, my_numbers = parse_card(card)
        copies[card_id] += 1
        for won_card_id in range(card_id+1, card_id+1+len(winning_numbers & my_numbers)):
            copies[won_card_id] += copies[card_id]
    return sum(copies.values())


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
