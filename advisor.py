# advisor.py

from calculator import simulate
from opponent_analyzer import analyze_opponent
from card import Card, SUIT_MAP, RANKS

def get_card_input(prompt, used_cards=[]):
    while True:
        try:
            entry = input(prompt).strip()
            if entry == '':
                return None
            rank = entry[:-1].upper()
            suit = entry[-1].lower()

            if rank not in RANKS:
                print(f"  ❌ Invalid rank '{rank}'. Use: 2-10, J, Q, K, A")
                continue
            if suit not in SUIT_MAP:
                print(f"  ❌ Invalid suit '{suit}'. Use: s, h, d, c")
                continue

            card = Card(rank, suit)

            # check for duplicates
            for used in used_cards:
                if used.rank == card.rank and used.suit == card.suit:
                    print(f"  ❌ {card} is already in play! Pick a different card.")
                    card = None
                    break

            if card is None:
                continue

            return card
        except:
            print("  ❌ Invalid input. Example: As, Kh, 10d")

def get_recommendation(win_pct, opponent_strength, bluff_pct):
    # if high bluff probability, treat opponent as weaker
    if bluff_pct >= 40:
        opponent_strength = 'weak'

    if win_pct > 70 and opponent_strength in ['very weak', 'weak']:
        return '🟢 RAISE', 'Strong hand + opponent likely bluffing — raise to take the pot!'
    elif win_pct > 70 and opponent_strength == 'medium':
        return '🟢 RAISE', 'You have a strong hand — raise to build the pot!'
    elif win_pct > 70 and opponent_strength == 'strong':
        return '🟡 CALL', 'You both have strong hands — proceed with caution!'
    elif win_pct > 50 and opponent_strength in ['very weak', 'weak']:
        return '🟢 CALL', 'You have the edge — calling is safe here!'
    elif win_pct > 50 and opponent_strength == 'medium':
        return '🟡 CALL', 'Roughly even — calling is reasonable but be careful!'
    elif win_pct > 50 and opponent_strength == 'strong' and bluff_pct >= 20:
        return '🟡 CALL', 'Opponent looks strong but there is a chance of bluffing!'
    elif win_pct > 50 and opponent_strength == 'strong':
        return '🔴 FOLD', 'Opponent likely has a strong hand — not worth the risk!'
    elif win_pct > 30:
        return '🔴 FOLD', 'Your win chance is low — save your chips!'
    else:
        return '🔴 FOLD', 'Very low win chance — fold and wait for a better hand!'

def run_advisor():
    print("=" * 40)
    print("     🃏 Poker Decision Advisor 🃏")
    print("=" * 40)
    print("Card format: As = A♠  Kh = K♥  10d = 10♦  Jc = J♣")
    print("Suits: s = ♠  h = ♥  d = ♦  c = ♣")
    print()

    # get your hole cards
    used_cards = []
    print("--- YOUR HAND ---")
    card1 = get_card_input("  Your card 1: ", used_cards)
    used_cards.append(card1)
    card2 = get_card_input("  Your card 2: ", used_cards)
    used_cards.append(card2)
    hole_cards = [card1, card2]
    print(f"  Your hand: {card1} {card2}")

    # get community cards
    print("\n--- COMMUNITY CARDS (press Enter to skip) ---")
    print("Suits: s = ♠  h = ♥  d = ♦  c = ♣")
    community_cards = []
    labels = ['Flop 1', 'Flop 2', 'Flop 3', 'Turn', 'River']
    for label in labels:
        card = get_card_input(f"  {label}: ", used_cards)
        if card is None:
            break
        community_cards.append(card)
        used_cards.append(card)

    # get number of opponents
    while True:
        try:
            num_opponents = int(input("\n  How many opponents? (1-8): "))
            if 1 <= num_opponents <= 8:
                break
            print("  ❌ Please enter between 1 and 8")
        except:
            print("  ❌ Invalid input")

    # get blinds and pot
    print("\n--- BLIND INFO ---")
    small_blind = float(input("  Small blind amount: ").strip())
    big_blind = float(input("  Big blind amount: ").strip())
    print(f"  Starting pot: {small_blind + big_blind}")
    pot_size = float(input("  Current pot size: ").strip())

    # get opponent actions
    print("\n--- OPPONENT ACTIONS (press Enter if street not reached yet) ---")
    print("  Actions: bet, call, check, fold, raise")
    preflop = input("  Preflop action: ").strip()
    flop = input("  Flop action: ").strip()
    turn = input("  Turn action (press Enter if deciding at flop): ").strip()
    river = input("  River action (press Enter if deciding at turn or flop): ").strip()

    # calculate your win %
    print("\n⏳ Analyzing...")
    result = simulate(hole_cards, community_cards, num_opponents)
    win_pct = result['win']

    # predict opponent strength (silently)
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    opponent_strength, bluff_pct = analyze_opponent(preflop, flop, turn, river, pot_size, num_opponents)
    sys.stdout = old_stdout

    # get recommendation
    action, reason = get_recommendation(win_pct, opponent_strength, bluff_pct)

    # display results
    print()
    print("=" * 40)
    print("         📊 FULL ANALYSIS")
    print("=" * 40)
    print(f"  Your win probability:  {win_pct}%")
    print(f"  Opponent likely has:   {opponent_strength.upper()} hand")
    print()
    print(f"  Recommendation: {action}")
    print(f"  Reason: {reason}")
    print("=" * 40)
