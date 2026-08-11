# tutor.py

import streamlit as st
from card import Card, SUIT_MAP, RANKS
from calculator import simulate
from opponent_analyzer import analyze_opponent
from advisor import get_recommendation
from collections import Counter

POSITIONS = ['UTG', 'UTG+1', 'MP', 'MP+1', 'HJ', 'CO', 'Button', 'SB', 'BB']

POSITION_TIPS = {
    'UTG': '😬 You are first to act — play tight, only strong hands!',
    'UTG+1': '😬 Early position — still play tight, many players behind you.',
    'MP': '😐 Middle position — you can play a wider range of hands.',
    'MP+1': '😐 Middle position — slightly more flexibility than UTG.',
    'HJ': '🙂 Hijack — good position, starting to open up your range.',
    'CO': '😊 Cutoff — great position! One before the dealer.',
    'Button': '😎 Button — BEST position! You act last on every street after preflop.',
    'SB': '😕 Small Blind — you act first after preflop, tough position.',
    'BB': '😕 Big Blind — you already put money in, defend wisely.'
}

HAND_TIPS = {
    (12, 12): "👑 Pocket Aces — the best starting hand! Always raise!",
    (11, 11): "🔥 Pocket Kings — second best hand! Raise strong!",
    (10, 10): "💪 Pocket Queens — very strong! Raise!",
    (9, 9): "💪 Pocket Jacks — strong but be careful of overcards!",
    (8, 8): "👍 Pocket Tens — solid hand, raise or call.",
}

RANK_ORDER = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']

RANK_OPTIONS = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
SUIT_OPTIONS = {'♠': 's', '♥': 'h', '♦': 'd', '♣': 'c'}
ACTION_OPTIONS = ['', 'bet', 'call', 'check', 'fold', 'raise']

def card_selector(label, key):
    col1, col2 = st.columns(2)
    with col1:
        rank = st.selectbox(f"{label} Rank", RANK_OPTIONS, key=f"{key}_rank")
    with col2:
        suit_label = st.selectbox(f"{label} Suit", list(SUIT_OPTIONS.keys()), key=f"{key}_suit")
    suit = SUIT_OPTIONS[suit_label]
    return Card(rank, suit)

def get_preflop_tier(card1, card2):
    r1 = card1.rank
    r2 = card2.rank
    suited = card1.suit == card2.suit
    ranks = tuple(sorted([r1, r2], key=lambda r: RANK_ORDER.index(r), reverse=True))

    # pairs
    if r1 == r2:
        if r1 in ['A', 'K', 'Q', 'J']:
            return 'S', '👑 Tier S — ALWAYS RAISE from any position!'
        if r1 == '10':
            return 'A', '🔥 Tier A — Raise from any position!'
        if r1 in ['9', '8']:
            return 'B', '💪 Tier B — Open raise, be selective with 3-bets.'
        return 'C', '😐 Tier C — Small pair, play carefully.'

    # non-pairs
    if ranks == ('A', 'K'):
        return 'S', '👑 Tier S — ALWAYS RAISE from any position!'
    if ranks in [('A', 'Q'), ('A', 'J'), ('K', 'Q')]:
        return 'A', '🔥 Tier A — Raise from any position!'
    if ranks in [('A', '10'), ('K', 'J'), ('Q', 'J'), ('J', '10')]:
        return 'B', '💪 Tier B — Raise, analyze board postflop.'
    if ranks in [('K', '10'), ('Q', '10'), ('J', '9'), ('10', '9')]:
        return 'C', '🟡 Tier C — Playable, raise from late position.'
    if r1 == 'A' or r2 == 'A':
        return 'C', '🃏 Ace high — playable but proceed with caution.'
    if suited and abs(RANK_ORDER.index(r1) - RANK_ORDER.index(r2)) <= 2:
        return 'C', '🎨 Suited connector — playable from late position.'

    return 'D', '🔴 Weak hand — check or fold in most situations.'

def get_hand_tip(card1, card2):
    tier, tier_msg = get_preflop_tier(card1, card2)
    vals = tuple(sorted([card1.value, card2.value], reverse=True))

    if vals in HAND_TIPS:
        return f"{HAND_TIPS[vals]}\n\n{tier_msg}"
    if card1.value == card2.value:
        return f"🎯 Pocket {card1.rank}s — a pair! {tier_msg}"
    if card1.suit == card2.suit:
        if card1.value >= 10 and card2.value >= 10:
            return f"✨ Suited broadway cards! {tier_msg}"
        return f"🎨 Suited cards — flush potential! {tier_msg}"
    if abs(card1.value - card2.value) <= 2:
        return f"🔗 Connected cards — straight draw potential! {tier_msg}"
    if card1.value == 12 or card2.value == 12:
        return f"🃏 Ace high. {tier_msg}"
    return f"⚠️ Weak starting hand. {tier_msg}"

def get_street_tip(community_cards, hole_cards):
    all_cards = hole_cards + community_cards
    suits = [c.suit for c in all_cards]
    ranks = [c.value for c in all_cards]
    tips = []

    suit_counts = Counter(suits)
    if max(suit_counts.values()) >= 5:
        tips.append("🎨 You have a FLUSH!")
    elif max(suit_counts.values()) >= 4:
        tips.append("🎨 You have a flush draw! One more card of the same suit wins!")

    rank_counts = Counter(ranks)
    counts = sorted(rank_counts.values(), reverse=True)
    if counts[0] == 4:
        tips.append("👑 FOUR OF A KIND! Incredible hand!")
    elif counts[0] == 3 and len(counts) > 1 and counts[1] == 2:
        tips.append("🏠 FULL HOUSE! Very strong hand!")
    elif counts[0] == 3:
        tips.append("3️⃣ THREE OF A KIND! Strong hand!")
    elif counts[0] == 2 and len(counts) > 1 and counts[1] == 2:
        tips.append("✌️ TWO PAIR! Decent hand.")
    elif counts[0] == 2:
        tips.append("1️⃣ ONE PAIR — keep an eye on the board.")
    else:
        tips.append("⚠️ No pair yet — you need to hit something!")

    return tips

def get_advice(win_pct, strength, bluff_pct, position=None, opponent_action=None):
    action, reason = get_recommendation(win_pct, strength, bluff_pct, position=position, opponent_action=opponent_action)
    if "RAISE" in action:
        st.success(f"👉 {action}")
    elif "CALL" in action or "CHECK" in action:
        st.warning(f"👉 {action}")
    else:
        st.error(f"👉 {action}")
    st.write(f"**Reason:** {reason}")

def run_tutor():
    st.header("🎓 Poker Tutor — Step by Step")
    st.markdown("*A guided walkthrough for beginners!*")
    st.divider()

    # ── SETUP ────────────────────────────────────────────
    st.subheader("⚙️ Game Setup")

    col1, col2 = st.columns(2)
    with col1:
        my_position = st.selectbox("Your Position", POSITIONS, index=6)
    with col2:
        total_players = st.slider("Total Players at Table", 2, 9, 9)

    col1, col2 = st.columns(2)
    with col1:
        small_blind = st.number_input("Small Blind", min_value=0.5, value=1.0, step=0.5)
    with col2:
        big_blind = st.number_input("Big Blind", min_value=1.0, value=2.0, step=1.0)

    st.info(POSITION_TIPS[my_position])
    st.divider()

    # ── PREFLOP ──────────────────────────────────────────
    st.subheader("🂠 Preflop — Your Hole Cards")

    col1, col2 = st.columns(2)
    with col1:
        card1 = card_selector("Card 1", "tutor_hole1")
    with col2:
        card2 = card_selector("Card 2", "tutor_hole2")

    hole_cards = [card1, card2]

    if card1.rank == card2.rank and card1.suit == card2.suit:
        st.error("❌ Both cards cannot be the same!")
        return

    st.success(f"Your hand: {card1} {card2}")
    st.info(get_hand_tip(card1, card2))

    max_to_flop = max(2, total_players - 1)
    players_to_flop = st.slider("How many players going to flop?", 1, max_to_flop, min(max_to_flop, 3))

    st.subheader("Opponent Preflop Action")
    preflop_action = st.selectbox("What did opponent do preflop?", ACTION_OPTIONS, key="tutor_preflop")

    if st.button("Get Preflop Advice 🎯"):
        with st.spinner("Analyzing..."):
            result = simulate(hole_cards, [], players_to_flop - 1)
            win_pct = result['win']

        st.metric("Your Win Probability", f"{win_pct}%")

        tier, tier_msg = get_preflop_tier(card1, card2)

        import io, sys
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        strength, bluff_pct = analyze_opponent(preflop_action, '', '', '', small_blind + big_blind, players_to_flop - 1)
        sys.stdout = old_stdout

        # override for strong hands
        if tier == 'S':
            st.success("👉 🟢 RAISE")
            st.write("**Reason:** Tier S hand — always raise preflop from any position!")
        elif tier == 'A' and my_position not in ['UTG', 'UTG+1']:
            st.success("👉 🟢 RAISE")
            st.write("**Reason:** Tier A hand — raise from this position!")
        elif tier == 'D':
            st.error("👉 🔴 FOLD")
            st.write("**Reason:** Weak hand — not worth playing in most situations.")
        else:
            get_advice(win_pct, strength, bluff_pct, position=my_position, opponent_action=preflop_action)

        if my_position == 'Button':
            st.info("💡 You're on the Button — use your position advantage!")
        elif my_position in ['SB', 'BB']:
            st.info("💡 You're in the blinds — be selective about defending.")
        elif my_position in ['UTG', 'UTG+1']:
            st.info("💡 Early position — only continue with strong hands.")

    st.divider()

    # ── FLOP ─────────────────────────────────────────────
    st.subheader("🃏 Flop")
    st.caption("Enter the 3 flop cards")

    col1, col2, col3 = st.columns(3)
    with col1:
        f1 = card_selector("Flop 1", "tutor_f1")
    with col2:
        f2 = card_selector("Flop 2", "tutor_f2")
    with col3:
        f3 = card_selector("Flop 3", "tutor_f3")

    flop_cards = [f1, f2, f3]

    max_to_turn = max(2, players_to_flop)
    players_to_turn = st.slider("How many players going to turn?", 1, max_to_turn, min(max_to_turn, 2))
    flop_action = st.selectbox("Opponent flop action", ACTION_OPTIONS, key="tutor_flop_action")

    if st.button("Get Flop Advice 🎯"):
        with st.spinner("Analyzing..."):
            result = simulate(hole_cards, flop_cards, players_to_turn - 1)
            win_pct = result['win']

        st.metric("Your Win Probability", f"{win_pct}%")

        tips = get_street_tip(flop_cards, hole_cards)
        for tip in tips:
            st.info(tip)

        import io, sys
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        strength, bluff_pct = analyze_opponent(preflop_action, flop_action, '', '', small_blind + big_blind, players_to_turn - 1)
        sys.stdout = old_stdout

        get_advice(win_pct, strength, bluff_pct, position=my_position, opponent_action=flop_action)

    st.divider()

    # ── TURN ─────────────────────────────────────────────
    st.subheader("🃏 Turn")
    st.caption("Enter the turn card")

    turn_card = card_selector("Turn Card", "tutor_turn")

    max_to_river = max(2, players_to_turn)
    players_to_river = st.slider("How many players going to river?", 1, max_to_river, min(max_to_river, 2))
    turn_action = st.selectbox("Opponent turn action", ACTION_OPTIONS, key="tutor_turn_action")

    if st.button("Get Turn Advice 🎯"):
        community = flop_cards + [turn_card]
        with st.spinner("Analyzing..."):
            result = simulate(hole_cards, community, players_to_river - 1)
            win_pct = result['win']

        st.metric("Your Win Probability", f"{win_pct}%")

        tips = get_street_tip(community, hole_cards)
        for tip in tips:
            st.info(tip)

        import io, sys
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        strength, bluff_pct = analyze_opponent(preflop_action, flop_action, turn_action, '', small_blind + big_blind, players_to_river - 1)
        sys.stdout = old_stdout

        get_advice(win_pct, strength, bluff_pct, position=my_position, opponent_action=turn_action)

    st.divider()

    # ── RIVER ────────────────────────────────────────────
    st.subheader("🃏 River")
    st.caption("Enter the river card")

    river_card = card_selector("River Card", "tutor_river")
    river_action = st.selectbox("Opponent river action", ACTION_OPTIONS, key="tutor_river_action")

    if st.button("Get River Advice 🎯"):
        community = flop_cards + [turn_card, river_card]
        with st.spinner("Analyzing..."):
            result = simulate(hole_cards, community, players_to_river - 1)
            win_pct = result['win']

        st.metric("Your Win Probability", f"{win_pct}%")

        tips = get_street_tip(community, hole_cards)
        for tip in tips:
            st.info(tip)

        import io, sys
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        strength, bluff_pct = analyze_opponent(preflop_action, flop_action, turn_action, river_action, small_blind + big_blind, players_to_river - 1)
        sys.stdout = old_stdout

        get_advice(win_pct, strength, bluff_pct, position=my_position, opponent_action=river_action)

        st.divider()
        st.subheader("🏁 Final Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Final Win %", f"{win_pct}%")
        col2.metric("Opponent Strength", strength.upper())
        col3.metric("Bluff Probability", f"{bluff_pct}%")
