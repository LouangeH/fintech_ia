import redis
import joblib
import numpy as np
import shap
import json
import os
from datetime import datetime
import pandas as pd

# Charger le modèle XGBoost
MODEL_PATH = os.path.join("ai_models", "fraud_model_xgb.pkl")
model = joblib.load(MODEL_PATH)

# Initialiser SHAP
explainer = shap.TreeExplainer(model)

# Connecter à Redis
r = redis.Redis()

# Simuler une base de données d'historique utilisateur
if not os.path.exists("user_profiles.csv"):
    df_init = pd.DataFrame(columns=["user_id", "amount"])
    df_init.to_csv("user_profiles.csv", index=False)

print("✅ IA Worker en écoute sur Redis Stream 'transactions'...")

while True:
    try:
        # Lire la prochaine transaction depuis Redis stream
        results = r.xread({b"transactions": b"$"}, block=0, count=1)
        for stream, messages in results:
            for msg_id, msg_data in messages:
                # Convertir en dict Python
                data = {k.decode(): float(v.decode()) for k, v in msg_data.items()}

                user_id = int(data["user_id"])
                features = [
                    "amount", "type_encoded", "location_encoded", "time_encoded",
                    "channel_encoded", "balance_before", "balance_after",
                    "is_weekend", "client_age_group"
                ]

                X = np.array([[data[f] for f in features]])

                # Prédiction
                prediction = model.predict(X)[0]
                confidence = model.predict_proba(X)[0][1]

                # SHAP Explanation
                shap_values = explainer.shap_values(X)
                explanation = dict(zip(features, shap_values[0].tolist()))

                # Profiling utilisateur (statistique de comportement)
                df_user = pd.read_csv("user_profiles.csv")
                df_same_user = df_user[df_user["user_id"] == user_id]
                profiling_alert = False

                if len(df_same_user) >= 5:
                    avg = df_same_user["amount"].mean()
                    std = df_same_user["amount"].std()
                    if std > 0 and abs(data["amount"] - avg) > 3 * std:
                        profiling_alert = True

                # Ajouter cette transaction au profil
                df_user = df_user.append({"user_id": user_id, "amount": data["amount"]}, ignore_index=True)
                df_user.to_csv("user_profiles.csv", index=False)

                # Afficher le résultat
                print(f"🧾 Transaction reçue de l'utilisateur {user_id}")
                print(f"  ➤ Fraude : {bool(prediction)}")
                print(f"  ➤ Confiance : {round(confidence, 2)}")
                if profiling_alert:
                    print("  ⚠️ Comportement anormal détecté pour cet utilisateur !")
                print(f"  ➤ Facteurs SHAP : {json.dumps(explanation, indent=2)}")
                print("-" * 60)

    except Exception as e:
        print(f"❌ Erreur : {str(e)}")
