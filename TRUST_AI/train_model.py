import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle

# Sample Data (Expanded for demonstration)
data = {
    'text': [
        "Congratulations! You've won a $1000 gift card. Click here.",
        "Your bank account has been suspended. Verify now.",
        "Breaking: Local elections scheduled for next month.",
        "Scientists discover new planet in habitable zone.",
        "URGENT: Your package delivery failed. Update info.",
        "Win a brand new car! Entry is free.",
        "The economy grew by 2% last quarter.",
        "School remains closed due to heavy snow.",
        "Limited time offer! Buy one get one free.",
        "Warning: suspicious activity detected on your account.",
        "NASA announces mission to Mars.",
        "New library opening downtown next week.",
        "Get rich quick with this one simple trick!",
        "IRS warning: Unpaid taxes. Call this number immediately.",
        "Exclusive deal just for you, sign up now.",
        "Community meeting at the town hall tonight.",
        "Update your password to prevent account lockout.",
        "Local sports team advances to the finals."
    ],
    'label': [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0]  # 1: Fake/Scam, 0: Real
}

df = pd.DataFrame(data)

# Preprocessing
df['text'] = df['text'].str.lower()

# Vectorization
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df['text'])
y = df['label']

# Model Training
model = MultinomialNB()
model.fit(X, y)

# Save Model and Vectorizer
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("Model and vectorizer saved successfully to model.pkl and vectorizer.pkl")
