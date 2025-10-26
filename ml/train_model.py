import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
import joblib

# Load sample data
data = pd.read_csv("data/user_learning_data.csv")

# Features and target
X = data[["response_time", "accuracy", "hints_used", "question_difficulty"]]
y = data["next_difficulty"]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train model
model = DecisionTreeClassifier(max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Save model and scaler
joblib.dump(model, "ml/difficulty_model.pkl")
joblib.dump(scaler, "ml/scaler.pkl")

print("✅ Model trained and saved!")
