# deck.py

import random
from card import Card, SUITS, RANKS

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in SUITS for rank in RANKS]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num):
        dealt = self.cards[:num]
        self.cards = self.cards[num:]
        return dealt

    def remove_cards(self, cards):
        for card in cards:
            self.cards = [c for c in self.cards if not (c.rank == card.rank and c.suit == card.suit)]

    def __repr__(self):
        return f"Deck({len(self.cards)} cards remaining)"
