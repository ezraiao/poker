# evaluator.py

from collections import Counter

def get_hand_rank(hand):
    ranks = sorted([card.value for card in hand], reverse=True)
    suits = [card.suit for card in hand]
    rank_counts = Counter(ranks)
    counts = sorted(rank_counts.values(), reverse=True)

    is_flush = len(set(suits)) == 1
    is_straight = (len(set(ranks)) == 5 and ranks[0] - ranks[4] == 4)

    if is_flush and is_straight:
        return (8, ranks)
    if counts[0] == 4:
        return (7, ranks)
    if counts[0] == 3 and counts[1] == 2:
        return (6, ranks)
    if is_flush:
        return (5, ranks)
    if is_straight:
        return (4, ranks)
    if counts[0] == 3:
        return (3, ranks)
    if counts[0] == 2 and counts[1] == 2:
        return (2, ranks)
    if counts[0] == 2:
        return (1, ranks)
    return (0, ranks)

def compare_hands(hand1, hand2):
    rank1 = get_hand_rank(hand1)
    rank2 = get_hand_rank(hand2)
    if rank1 > rank2:
        return 1   # hand1 wins
    elif rank2 > rank1:
        return -1  # hand2 wins
    else:
        return 0   # tie
