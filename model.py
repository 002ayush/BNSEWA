# train_model.py
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load dataset
data = pd.read_csv("FIR_DATASET.csv")
data.dropna(inplace=True)

# Feature extraction
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(data['Offense'])

# Encoding categorical outputs
encoders = {}
y = {}
for column in ['Punishment', 'Cognizable', 'Bailable', 'Court']:
    encoders[column] = LabelEncoder()
    y[column] = encoders[column].fit_transform(data[column])

# Prepare training data
X_train, X_test, y_train, y_test = train_test_split(X, pd.DataFrame(y), test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model, vectorizer, and encoders
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)
with open("encoders.pkl", "wb") as f:
    pickle.dump(encoders, f)

print("✅ Model and components saved.")
