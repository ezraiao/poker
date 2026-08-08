# generate_data.py

import pandas as pd
import numpy as np
import random

random.seed(42)

def generate_hand(num_samples=50000):
    data = []

    for _ in range(num_samples):
        # opponent hand strength (0-1)
        hand_strength = round(random.uniform(0, 1), 2)

        # generate actions based on hand strength
        if hand_strength > 0.75:        # strong hand
            preflop = random.choice(['raise', 'raise', 'raise', 'call'])
            flop = random.choice(['bet', 'bet', 'raise', 'call'])
            turn = random.choice(['bet', 'raise', 'bet'])
            river = random.choice(['bet', 'raise', 'bet'])
        elif hand_strength > 0.5:       # medium hand
            preflop = random.choice(['call', 'call', 'raise', 'fold'])
            flop = random.choice(['call', 'check', 'bet', 'fold'])
            turn = random.choice(['call', 'check', 'fold', 'bet'])
            river = random.choice(['call', 'check', 'fold'])
        elif hand_strength > 0.25:      # weak hand
            preflop = random.choice(['call', 'fold', 'fold', 'call'])
            flop = random.choice(['check', 'fold', 'call', 'check'])
            turn = random.choice(['check', 'fold', 'fold', 'call'])
            river = random.choice(['check', 'fold', 'fold'])
        else:                           # very weak hand
            preflop = random.choice(['fold', 'fold', 'fold', 'call'])
            flop = random.choice(['fold', 'check', 'fold'])
            turn = random.choice(['fold', 'check', 'fold'])
            river = random.choice(['fold', 'check'])

        # pot size relative to blinds
        pot_size = round(random.uniform(2, 20) * hand_strength + random.uniform(1, 5), 2)

        # number of players still in
        players_remaining = random.randint(1, 8)

        data.append({
            'hand_strength': hand_strength,
            'preflop_action': preflop,
            'flop_action': flop,
            'turn_action': turn,
            'river_action': river,
            'pot_size': pot_size,
            'players_remaining': players_remaining
        })

    return pd.DataFrame(data)

df = generate_hand()
df.to_csv('poker_data.csv', index=False)

print(f"✅ Generated {len(df)} hands!")
print(f"\nSample data:")
print(df.head())
print(f"\nHand strength distribution:")
print(df['hand_strength'].describe())
