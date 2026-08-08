# card.py

SUITS = ['♠', '♥', '♦', '♣']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

SUIT_MAP = {
    # letters
    's': '♠', 'spade': '♠', 'spades': '♠',
    'h': '♥', 'heart': '♥', 'hearts': '♥',
    'd': '♦', 'diamond': '♦', 'diamonds': '♦',
    'c': '♣', 'club': '♣', 'clubs': '♣',
    # symbols (for internal use)
    '♠': '♠', '♥': '♥', '♦': '♦', '♣': '♣'
}

class Card:
    def __init__(self, rank, suit):
        self.rank = rank.upper()
        self.suit = SUIT_MAP[suit.lower()]
        self.value = RANKS.index(self.rank)

    def __repr__(self):
        return f"{self.rank}{self.suit}"
