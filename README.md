# 🃏 Poker AI Assistant

> *Because winning isn't just luck — it's math.*

A personal project leveraging data-driven analysis and machine learning to improve poker decision-making, one hand at a time.

---

## 🎯 Overview

This project is built in four phases:

### Phase 1 — Hand Equity Calculator 🧮 ✅ COMPLETED
A tool that calculates the **winning probability** of any given hand against a range of opponent hands, based on current board state and remaining deck composition.

### Phase 2 — Opponent Behavior Analysis 🤖 ✅ COMPLETED
A machine learning model that infers likely **opponent hand ranges** and **bluff probability** by analyzing their betting patterns and in-game actions.

### Phase 3 — Decision Advisor 🧠 ✅ COMPLETED
Combines Phase 1 and Phase 2 to give a final recommendation — **Call, Fold, or Raise** — based on your win probability and opponent's predicted hand strength.

### Phase 4 — Tutor Mode 🎓 ✅ COMPLETED
A beginner-friendly web app that guides players step by step through every street — Preflop, Flop, Turn, and River — with real-time tips, hand strength analysis, and position-aware advice.

---

## ⚙️ Setup Before Running

Run these once to generate the data and train the model:
```bash
python3 generate_data.py
python3 model.py
```

---

## 🚀 How To Run

**Terminal version:**
```bash
python3 main.py
```
Choose from 3 modes:
- **Mode 1** — Hand Equity Calculator
- **Mode 2** — Opponent Analyzer
- **Mode 3** — Decision Advisor

**Web app version:**
```bash
.venv/bin/streamlit run app.py
```
Choose from 4 modes:
- **Mode 1** — Hand Equity Calculator
- **Mode 2** — Opponent Analyzer
- **Mode 3** — Decision Advisor
- **Mode 4** — 🎓 Poker Tutor (Beginner Friendly)

---

## 🎯 Goals

- ♠️ Apply probability theory and combinatorics to real-time poker scenarios
- ♥️ Develop a predictive model trained on opponent action data
- ♦️ Build a practical tool that bridges statistical analysis with gameplay strategy
- ♣️ Make poker strategy accessible to beginners through guided tutor mode

---

## 🛠️ Built With
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)

---

## 📌 Status
- ✅ Phase 1 — Completed
- ✅ Phase 2 — Completed
- ✅ Phase 3 — Completed
- ✅ Phase 4 — Completed

---

## 🤝 Connect With Me
If you'd like to connect, feel free to reach out on [LinkedIn](https://www.linkedin.com/in/cheng-iao-3994b4382)!
