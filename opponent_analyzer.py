# opponent_analyzer.py

import pickle
from sklearn.preprocessing import LabelEncoder

ACTIONS = ['bet', 'call', 'check', 'fold', 'raise']

def encode_action(action):
    le = LabelEncoder()
    le.fit(ACTIONS)
    if action == '' or action is None:
        return encode_action('check')
    return le.transform([action.lower()])[0]

def calculate_bluff_probability(preflop, flop, turn, river, pot_size, players_remaining):
    bluff_score = 0

    # check-raise on river is a classic bluff tell
    if turn in ['check', ''] and river == 'raise':
        bluff_score += 30

    # raising on river after passive play is suspicious
    if preflop in ['call', 'check'] and flop in ['check', 'call'] and river == 'raise':
        bluff_score += 25

    # less likely to bluff with many players
    if players_remaining > 3:
        bluff_score -= 15
    elif players_remaining == 1:
        bluff_score += 10

    # less likely to bluff in a huge pot
    if pot_size > 500:
        bluff_score -= 20
    elif pot_size < 50:
        bluff_score += 10

    # consistent aggression is less likely a bluff
    aggressive_actions = [preflop, flop, turn, river]
    raise_count = aggressive_actions.count('raise') + aggressive_actions.count('bet')
    if raise_count >= 3:
        bluff_score -= 15

    # sudden aggression after passive play is suspicious
    passive_streets = [a for a in [preflop, flop, turn] if a in ['check', 'call', '']]
    if len(passive_streets) >= 2 and river == 'raise':
        bluff_score += 20

    # clamp between 0 and 100
    return max(0, min(100, bluff_score))

def analyze_opponent(preflop, flop, turn, river, pot_size, players_remaining):
    with open('poker_model.pkl', 'rb') as f:
        model = pickle.load(f)

    features = [[
        encode_action(preflop),
        encode_action(flop),
        encode_action(turn),
        encode_action(river),
        pot_size,
        players_remaining
    ]]

    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    classes = model.classes_

    # calculate bluff probability
    bluff_pct = calculate_bluff_probability(preflop, flop, turn, river, pot_size, players_remaining)

    print("\n" + "=" * 40)
    print("       🔍 OPPONENT ANALYSIS")
    print("=" * 40)
    print(f"  Predicted hand strength: {prediction.upper()}")
    print(f"  Bluff probability:       {bluff_pct}%")
    print()
    print("  Probability breakdown:")
    for cls, prob in sorted(zip(classes, probabilities), key=lambda x: x[1], reverse=True):
        bar = "█" * int(prob * 20)
        print(f"  {cls:<10} {bar} {round(prob * 100, 1)}%")

    # bluff warning
    print()
    if bluff_pct >= 40:
        print("  ⚠️  WARNING: High chance of bluff!")
        print("      Consider calling if your hand is decent.")
    elif bluff_pct >= 20:
        print("  ⚠️  Possible bluff — proceed with caution.")
    else:
        print("  ✅ Action pattern looks genuine.")

    print("=" * 40)

    return prediction, bluff_pct
