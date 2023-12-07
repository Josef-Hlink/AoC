#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 23 Day 7 - Camel Cards """

from paoc.helper import get_input, print_summary


class Hand:
    """ A hand consist of 5 cards (single characters), and an integer bid. """

    def __init__(self, cards: str, bid: str, rule_set: int = 1):
        assert rule_set in (1, 2), f'Invalid rule set'
        self.bid = int(bid)        
        self.cards = cards
        self.cards_order = '23456789TJQKA' if rule_set == 1 else 'J23456789TQKA'
        self.parsed_cards = self.cards if rule_set == 1 else self.replace_J(self.cards)

    @staticmethod
    def replace_J(cards: str) -> str:
        if 'J' not in cards: return cards
        if cards == 'JJJJJ': return '22222'
        card_counts = {card: cards.count(card) for card in set(cards) - {'J'}}
        return cards.replace('J', sorted(card_counts, key=lambda card: card_counts[card])[-1])

    @property
    def hand_type_strength(self) -> int:
        counts = tuple(sorted((self.parsed_cards.count(card) for card in set(self.parsed_cards))))
        return ((1,1,1,1,1), (1,1,1,2), (1,2,2), (1,1,3), (2,3), (1,4), (5,)).index(counts)

    def __lt__(self, other: "Hand") -> bool:
        if self.hand_type_strength != other.hand_type_strength:
            return self.hand_type_strength < other.hand_type_strength
        for s, o in zip(self.cards, other.cards):
            if self.cards_order.index(s) != self.cards_order.index(o):
                return self.cards_order.index(s) < self.cards_order.index(o)
        raise ValueError('Hands are the exact same')

def calc_total_winnings(hands: list[str], rule_set: int) -> int:
    return sum([i * hand.bid for i, hand in enumerate(sorted([Hand(*hand.split(), rule_set) for hand in hands]), start=1)])

def p1() -> any:
    return calc_total_winnings(get_input(7), rule_set=1)

def p2() -> any:
    return calc_total_winnings(get_input(7), rule_set=2)


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
