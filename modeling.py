import numpy as np
import pandas as pd
import joblib
import warnings
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import VotingClassifier
from catboost import CatBoostClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

warnings.filterwarnings("ignore")

# Load dataset
df = pd.read_csv("liver_cirrhosis.csv")

# Drop unnecessary columns
df.drop(columns=["N_Days", "Status", "Drug"], inplace=True)

# Convert Age from days to years
df["Age"] = (df["Age"] / 365).round().astype(int)

# Encode categorical variables
label_encoders = {}
categorical_cols = ["Sex", "Ascites", "Hepatomegaly", "Spiders", "Edema"]

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Define Features (X) and Target (y)
X = df.drop(columns=["Stage"])
y = df["Stage"]

# Ensure Stage values are mapped correctly (1, 2, 3, 4)
print("Unique Stages:", y.unique())  # Debugging check

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Feature Scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Define ML Models
catboost = CatBoostClassifier(verbose=0, random_seed=42)
xgboost = XGBClassifier(use_label_encoder=False, eval_metric="mlogloss", random_state=42)
lightgbm = LGBMClassifier(random_state=42)

# Voting Classifier
voting_clf = VotingClassifier(
    estimators=[("catboost", catboost), ("xgboost", xgboost), ("lightgbm", lightgbm)],
    voting="soft"
)

# Train the model
voting_clf.fit(X_train, y_train)

# Model Evaluation
y_pred = voting_clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\n✅ Accuracy:", accuracy)
print("\n✅ Classification Report:\n", classification_report(y_test, y_pred))
print("\n✅ Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Save Model and Preprocessing Objects
joblib.dump(voting_clf, "liver_cirrhosis_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")

print("\n✅ Model training complete. Files saved: 'liver_cirrhosis_model.pkl', 'scaler.pkl', 'label_encoders.pkl'")
