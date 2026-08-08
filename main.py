# main.py

from card import Card, SUIT_MAP, RANKS
from calculator import simulate
from advisor import run_advisor

def get_card_input(prompt, used_cards=[]):
    while True:
        try:
            entry = input(prompt).strip()
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

def get_community_cards(used_cards=[]):
    community = []
    print("\nEnter community cards (press Enter to skip):")
    print("Suits: s = ♠  h = ♥  d = ♦  c = ♣")
    labels = ['Flop 1', 'Flop 2', 'Flop 3', 'Turn', 'River']
    for label in labels:
        entry = input(f"  {label} (or press Enter to skip): ").strip()
        if entry == '':
            break
        rank = entry[:-1].upper()
        suit = entry[-1].lower()
        try:
            card = Card(rank, suit)
            # check for duplicates
            duplicate = False
            for used in used_cards:
                if used.rank == card.rank and used.suit == card.suit:
                    print(f"  ❌ {card} is already in play! Pick a different card.")
                    duplicate = True
                    break
            if duplicate:
                continue
            community.append(card)
            used_cards.append(card)
        except:
            print("  ❌ Skipping invalid card")
    return community

def analyze_mode():
    print("\n" + "=" * 40)
    print("       🔍 Opponent Analyzer")
    print("=" * 40)
    print("Actions: bet, call, check, fold, raise")
    print("Press Enter to skip streets not played yet")
    print()

    small_blind = float(input("  Small blind amount: ").strip())
    big_blind = float(input("  Big blind amount: ").strip())
    print(f"  Starting pot: {small_blind + big_blind}")

    preflop = input("  Opponent preflop action: ").strip()
    flop = input("  Opponent flop action: ").strip()
    turn = input("  Opponent turn action: ").strip()
    river = input("  Opponent river action: ").strip()

    pot_size = float(input("  Current pot size (or press Enter to use blinds): ").strip() or small_blind + big_blind)
    players = int(input("  Players remaining: ").strip())

    from opponent_analyzer import analyze_opponent
    analyze_opponent(preflop, flop, turn, river, pot_size, players)

def main():
    print("=" * 40)
    print("       🃏 Poker AI Assistant 🃏")
    print("=" * 40)
    print("1. Hand Equity Calculator")
    print("2. Opponent Analyzer")
    print("3. Decision Advisor (Phase 1 + Phase 2 combined)")
    print()

    choice = input("Choose mode (1, 2 or 3): ").strip()

    if choice == "1":
        print("\nCard format: rank + suit letter")
        print("Examples: As = A♠  Kh = K♥  10d = 10♦  Jc = J♣")
        print("Suits: s = ♠  h = ♥  d = ♦  c = ♣")
        print()

        # get hole cards
        used_cards = []
        print("Enter your 2 hole cards:")
        card1 = get_card_input("  Card 1: ", used_cards)
        used_cards.append(card1)
        card2 = get_card_input("  Card 2: ", used_cards)
        used_cards.append(card2)
        hole_cards = [card1, card2]
        print(f"  Your hand: {card1} {card2}")

        # get community cards
        community_cards = get_community_cards(used_cards)
        if community_cards:
            print(f"  Board: {' '.join(str(c) for c in community_cards)}")

        # get number of opponents
        while True:
            try:
                num_opponents = int(input("\nHow many opponents? (1-8): "))
                if 1 <= num_opponents <= 8:
                    break
                print("  ❌ Please enter a number between 1 and 8")
            except:
                print("  ❌ Please enter a valid number")

        # run simulation
        print(f"\n⏳ Running simulation...")
        result = simulate(hole_cards, community_cards, num_opponents)

        # display results
        print()
        print("=" * 40)
        print("           📊 RESULTS")
        print("=" * 40)
        print(f"  ✅ Win:  {result['win']}%")
        print(f"  🤝 Tie:  {result['tie']}%")
        print(f"  ❌ Loss: {result['loss']}%")
        print("=" * 40)

    elif choice == "2":
        analyze_mode()

    elif choice == "3":
        run_advisor()

    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
