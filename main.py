# main.py

from card import Card, SUIT_MAP, RANKS
from calculator import simulate

def get_card_input(prompt):
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

            return Card(rank, suit)
        except:
            print("  ❌ Invalid input. Example: As, Kh, 10d")

def get_community_cards():
    community = []
    print("\nEnter community cards (press Enter to skip):")
    labels = ['Flop 1', 'Flop 2', 'Flop 3', 'Turn', 'River']
    for label in labels:
        entry = input(f"  {label} (or press Enter to skip): ").strip()
        if entry == '':
            break
        rank = entry[:-1].upper()
        suit = entry[-1].lower()
        try:
            community.append(Card(rank, suit))
        except:
            print("  ❌ Skipping invalid card")
    return community

def main():
    print("=" * 40)
    print("       🃏 Poker Hand Calculator 🃏")
    print("=" * 40)
    print("Card format: rank + suit letter")
    print("Examples: As = A♠  Kh = K♥  10d = 10♦  2c = 2♣")
    print()

    # get hole cards
    print("Enter your 2 hole cards:")
    card1 = get_card_input("  Card 1: ")
    card2 = get_card_input("  Card 2: ")
    hole_cards = [card1, card2]
    print(f"  Your hand: {card1} {card2}")

    # get community cards
    community_cards = get_community_cards()
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

if __name__ == "__main__":
    main()
