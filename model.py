# model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import pickle

# load data
df = pd.read_csv('poker_data.csv')

# convert actions to numbers (ML can't read words)
le = LabelEncoder()
for col in ['preflop_action', 'flop_action', 'turn_action', 'river_action']:
    df[col] = le.fit_transform(df[col])

# convert hand strength to categories
def classify_strength(strength):
    if strength > 0.75:
        return 'strong'
    elif strength > 0.5:
        return 'medium'
    elif strength > 0.25:
        return 'weak'
    else:
        return 'very weak'

df['hand_category'] = df['hand_strength'].apply(classify_strength)

# features and target
X = df[['preflop_action', 'flop_action', 'turn_action', 'river_action', 'pot_size', 'players_remaining']]
y = df['hand_category']

# split into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# train the model
print("⏳ Training model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# test accuracy
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"✅ Model trained!")
print(f"📊 Accuracy: {round(accuracy * 100, 2)}%")

# save model
with open('poker_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("💾 Model saved to poker_model.pkl")
