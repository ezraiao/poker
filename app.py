# app.py

import streamlit as st
from card import Card, SUIT_MAP, RANKS
from calculator import simulate
from opponent_analyzer import analyze_opponent
from advisor import get_recommendation
from tutor import run_tutor

st.set_page_config(
    page_title="Poker AI Assistant",
    page_icon="🃏",
    layout="centered"
)

st.title("🃏 Poker AI Assistant")
st.markdown("> *Because winning isn't just luck — it's math.*")
st.divider()

mode = st.selectbox("Choose Mode", [
    "1️⃣ Hand Equity Calculator",
    "2️⃣ Opponent Analyzer",
    "3️⃣ Decision Advisor",
    "4️⃣ 🎓 Poker Tutor (Beginner Friendly)"
])

# ─── SHARED HELPERS ───────────────────────────────────────
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

def community_card_selector(used_cards):
    st.subheader("Community Cards")
    cards = []
    labels = ['Flop 1', 'Flop 2', 'Flop 3', 'Turn', 'River']
    cols = st.columns(5)
    for i, label in enumerate(labels):
        with cols[i]:
            include = st.checkbox(label, key=f"include_{label}")
            if include:
                rank = st.selectbox("Rank", RANK_OPTIONS, key=f"comm_{label}_rank")
                suit_label = st.selectbox("Suit", list(SUIT_OPTIONS.keys()), key=f"comm_{label}_suit")
                suit = SUIT_OPTIONS[suit_label]
                card = Card(rank, suit)
                # check duplicate
                is_dup = any(c.rank == card.rank and c.suit == card.suit for c in used_cards + cards)
                if is_dup:
                    st.error(f"Duplicate!")
                else:
                    cards.append(card)
    return cards

# ─── MODE 1: HAND EQUITY CALCULATOR ──────────────────────
if mode == "1️⃣ Hand Equity Calculator":
    st.header("Hand Equity Calculator 🧮")

    st.subheader("Your Hole Cards")
    col1, col2 = st.columns(2)
    with col1:
        card1 = card_selector("Card 1", "hole1")
    with col2:
        card2 = card_selector("Card 2", "hole2")

    hole_cards = [card1, card2]

    # check duplicate hole cards
    if card1.rank == card2.rank and card1.suit == card2.suit:
        st.error("❌ Your two hole cards cannot be the same!")
    else:
        st.success(f"Your hand: {card1} {card2}")
        community_cards = community_card_selector(hole_cards)

        num_opponents = st.slider("Number of Opponents", 1, 8, 1)

        if st.button("Calculate Win Probability 🎯"):
            with st.spinner("Running simulation..."):
                result = simulate(hole_cards, community_cards, num_opponents)

            st.divider()
            st.subheader("📊 Results")
            col1, col2, col3 = st.columns(3)
            col1.metric("✅ Win", f"{result['win']}%")
            col2.metric("🤝 Tie", f"{result['tie']}%")
            col3.metric("❌ Loss", f"{result['loss']}%")

# ─── MODE 2: OPPONENT ANALYZER ───────────────────────────
elif mode == "2️⃣ Opponent Analyzer":
    st.header("Opponent Analyzer 🔍")

    col1, col2 = st.columns(2)
    with col1:
        small_blind = st.number_input("Small Blind", min_value=0.5, value=1.0, step=0.5)
    with col2:
        big_blind = st.number_input("Big Blind", min_value=1.0, value=2.0, step=1.0)

    pot_size = st.number_input("Current Pot Size", min_value=0.0, value=small_blind + big_blind)
    players = st.slider("Players Remaining", 1, 8, 1)

    st.subheader("Opponent Actions")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        preflop = st.selectbox("Preflop", ACTION_OPTIONS)
    with col2:
        flop = st.selectbox("Flop", ACTION_OPTIONS)
    with col3:
        turn = st.selectbox("Turn", ACTION_OPTIONS)
    with col4:
        river = st.selectbox("River", ACTION_OPTIONS)

    if st.button("Analyze Opponent 🔍"):
        with st.spinner("Analyzing..."):
            strength, bluff_pct = analyze_opponent(preflop, flop, turn, river, pot_size, players)

        st.divider()
        st.subheader("📊 Results")
        col1, col2 = st.columns(2)
        col1.metric("Predicted Hand Strength", strength.upper())
        col2.metric("Bluff Probability", f"{bluff_pct}%")

        if bluff_pct >= 40:
            st.warning("⚠️ HIGH chance of bluff! Consider calling if your hand is decent.")
        elif bluff_pct >= 20:
            st.warning("⚠️ Possible bluff — proceed with caution.")
        else:
            st.success("✅ Action pattern looks genuine.")

# ─── MODE 3: DECISION ADVISOR ────────────────────────────
elif mode == "3️⃣ Decision Advisor":
    st.header("Decision Advisor 🧠")

    st.subheader("Your Hole Cards")
    col1, col2 = st.columns(2)
    with col1:
        card1 = card_selector("Card 1", "adv_hole1")
    with col2:
        card2 = card_selector("Card 2", "adv_hole2")

    hole_cards = [card1, card2]

    if card1.rank == card2.rank and card1.suit == card2.suit:
        st.error("❌ Your two hole cards cannot be the same!")
    else:
        st.success(f"Your hand: {card1} {card2}")
        community_cards = community_card_selector(hole_cards)

        num_opponents = st.slider("Number of Opponents", 1, 8, 1, key="adv_opponents")

        st.subheader("Blind Info")
        col1, col2 = st.columns(2)
        with col1:
            small_blind = st.number_input("Small Blind", min_value=0.5, value=1.0, step=0.5, key="adv_sb")
        with col2:
            big_blind = st.number_input("Big Blind", min_value=1.0, value=2.0, step=1.0, key="adv_bb")

        pot_size = st.number_input("Current Pot Size", min_value=0.0, value=small_blind + big_blind, key="adv_pot")

        st.subheader("Opponent Actions")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            preflop = st.selectbox("Preflop", ACTION_OPTIONS, key="adv_preflop")
        with col2:
            flop = st.selectbox("Flop", ACTION_OPTIONS, key="adv_flop")
        with col3:
            turn = st.selectbox("Turn", ACTION_OPTIONS, key="adv_turn")
        with col4:
            river = st.selectbox("River", ACTION_OPTIONS, key="adv_river")

        if st.button("Get Recommendation 🎯"):
            with st.spinner("Analyzing..."):
                result = simulate(hole_cards, community_cards, num_opponents)
                win_pct = result['win']

                import io, sys
                old_stdout = sys.stdout
                sys.stdout = io.StringIO()
                strength, bluff_pct = analyze_opponent(preflop, flop, turn, river, pot_size, num_opponents)
                sys.stdout = old_stdout

                action, reason = get_recommendation(win_pct, strength, bluff_pct)

            st.divider()
            st.subheader("📊 Full Analysis")
            col1, col2, col3 = st.columns(3)
            col1.metric("Your Win %", f"{win_pct}%")
            col2.metric("Opponent Strength", strength.upper())
            col3.metric("Bluff Probability", f"{bluff_pct}%")

            st.divider()
            if "RAISE" in action:
                st.success(f"Recommendation: {action}")
            elif "CALL" in action:
                st.warning(f"Recommendation: {action}")
            else:
                st.error(f"Recommendation: {action}")
            st.write(f"**Reason:** {reason}")

elif mode == "4️⃣ 🎓 Poker Tutor (Beginner Friendly)":
    run_tutor()
