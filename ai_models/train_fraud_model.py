# ai_models/train_fraud_model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

# 1. Charger les données depuis le CSV
data_path = os.path.join("data", "transactions_burundi_extended.csv")
df = pd.read_csv(data_path)

# 2. Séparer les features (X) et les labels (y)
X = df.drop(columns=["is_fraud"])   # toutes les colonnes sauf la cible
y = df["is_fraud"]                  # cible

# 3. Diviser les données en jeu d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Entraîner le modèle RandomForest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Évaluer les performances
y_pred = model.predict(X_test)
print("=== Évaluation du modèle ===")
print(classification_report(y_test, y_pred))

# 6. Sauvegarder le modèle entraîné dans un fichier
output_path = os.path.join("ai_models", "fraud_model_FBu.pkl")
joblib.dump(model, output_path)
print(f"✅ Modèle sauvegardé dans : {output_path}")
