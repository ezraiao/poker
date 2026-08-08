# calculator.py

import random
from deck import Deck
from card import Card
from evaluator import get_hand_rank

def simulate(hole_cards, community_cards=[], num_opponents=1, simulations=10000):
    wins = 0
    ties = 0

    for _ in range(simulations):
        deck = Deck()

        # remove known cards from deck
        known_cards = hole_cards + community_cards
        deck.remove_cards(known_cards)

        # shuffle remaining deck
        deck.shuffle()

        # fill community cards to 5
        remaining = 5 - len(community_cards)
        board = community_cards + deck.deal(remaining)

        # deal opponent hands
        opponents = []
        for _ in range(num_opponents):
            opponents.append(deck.deal(2))

        # evaluate my best 5 card hand
        my_best = get_hand_rank(hole_cards + board)

        # compare against all opponents
        i_win = True
        tie = False

        for opp in opponents:
            opp_best = get_hand_rank(opp + board)
            if opp_best > my_best:
                i_win = False
                break
            elif opp_best == my_best:
                tie = True
                i_win = False

        if i_win:
            wins += 1
        elif tie:
            ties += 1

    win_pct = (wins / simulations) * 100
    tie_pct = (ties / simulations) * 100
    loss_pct = 100 - win_pct - tie_pct

    return {
        'win': round(win_pct, 2),
        'tie': round(tie_pct, 2),
        'loss': round(loss_pct, 2)
    }
