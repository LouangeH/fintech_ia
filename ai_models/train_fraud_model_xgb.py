import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
from xgboost import XGBClassifier
import os

# === Étape 1 : Chargement des données ===
data_path = os.path.join("data", "transactions_burundi_extended.csv")
df = pd.read_csv(data_path)

# === Étape 2 : Définition des features ===
features = [
    "amount",
    "type_encoded",
    "location_encoded",
    "time_encoded",
    "channel_encoded",
    "balance_before",
    "balance_after",
    "is_weekend",
    "client_age_group"
]

X = df[features]
y = df["is_fraud"]

# === Étape 3 : Division des données ===
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# === Étape 4 : Entraînement du modèle XGBoost ===
model = XGBClassifier(
    use_label_encoder=False,
    eval_metric="logloss",
    random_state=42
)
model.fit(X_train, y_train)

# === Étape 5 : Évaluation du modèle ===
y_pred = model.predict(X_test)
print("=== Rapport de classification ===")
print(classification_report(y_test, y_pred))
print("=== Matrice de confusion ===")
print(confusion_matrix(y_test, y_pred))

# === Étape 6 : Sauvegarde du modèle ===
output_path = os.path.join("ai_models", "fraud_model_xgb.pkl")
joblib.dump(model, output_path)
print(f"✅ Modèle XGBoost sauvegardé dans : {output_path}")
