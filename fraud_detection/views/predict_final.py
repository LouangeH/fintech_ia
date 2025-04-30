# # fraud_detection/views.py

# import joblib
# import os
# import numpy as np
# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# # 1. Charger le modèle dès le chargement du module
# MODEL_PATH = os.path.join("ai_models", "fraud_model_FBu.pkl")
# model = joblib.load(MODEL_PATH)

# @api_view(['POST'])
# def prediction_fraude(request):
#     """
#     Utilise un modèle entraîné pour prédire si une transaction est frauduleuse.
#     """
#     # 2. Extraire les données depuis la requête JSON
#     try:
#         amount = float(request.data.get("amount", 0))
#         type_encoded = int(request.data.get("type_encoded", 0))
#         location_encoded = int(request.data.get("location_encoded", 0))
#         time_encoded = int(request.data.get("time_encoded", 0))
#     except (TypeError, ValueError):
#         return Response({"error": "Champs invalides ou manquants"}, status=400)

#     # 3. Construire l'entrée pour le modèle
#     features = np.array([[amount, type_encoded, location_encoded, time_encoded]])

#     # 4. Faire la prédiction
#     prediction = model.predict(features)[0]
#     probability = model.predict_proba(features)[0][1]  # probabilité d’être fraude

#     # 5. Retourner la réponse
#     return Response({
#         "fraud": bool(prediction),
#         "confidence": round(probability, 2)
#     })

import joblib
import os
import numpy as np
from rest_framework.decorators import api_view
from rest_framework.response import Response
from fraud_detection.serializers import TransactionInputSerializer
from fraud_detection.models import PredictionLog
import shap

# Charger le modèle
MODEL_PATH = os.path.join("ai_models", "fraud_model_xgb.pkl")
model = joblib.load(MODEL_PATH)

@api_view(['POST'])
def prediction_fraud(request):
    serializer = TransactionInputSerializer(data=request.data)
    
    if serializer.is_valid():
        # Extraire les données
        data = serializer.validated_data
        features = np.array([[data["amount"], data["type_encoded"],
                              data["location_encoded"], data["time_encoded"],
                                data["channel_encoded"], data["balance_before"],
                                data["balance_after"], data["is_weekend"],
                                data["client_age_group"]]])
        # Juste après validation du serializer
        alerts = []

        # REGLE : Retrait > 50 millions
        if data["type_encoded"] == 0 and data["amount"] > 50000000:
            alerts.append("Retrait supérieur à 50M FBu interdit")

        # REGLE : Dépôt via Lumicash > 3 millions
        if data["type_encoded"] == 1 and data["amount"] > 3000000:
            alerts.append("Dépôt via Lumicash > 3M FBu non autorisé")

        # REGLE : Heure > 17h
        if data["time_encoded"] > 17:
            alerts.append("Transaction effectuée après la fermeture des banques")
        
        # comportement utilisateur
        user_logs = PredictionLog.objects.filter(user_id="user_id")
        amounts = [log.amount for log in user_logs]
        if len(amounts) >= 5:
            avg = np.mean(amounts)
            std = np.std(amounts)
            if std > 0 and abs(data["amount"] - avg) > 3 * std:
                alerts.append("Montant inhabituel comparé à l’historique de l’utilisateur")

        # Faire prédiction
        prediction = model.predict(features)[0]
        confidence = model.predict_proba(features)[0][1]

        # Sauvegarder dans l'historique
        PredictionLog.objects.create(
            amount=data["amount"],
            type_encoded=data["type_encoded"],
            location_encoded=data["location_encoded"],
            time_encoded=data["time_encoded"],
            predicted_fraud=bool(prediction),
            confidence=confidence
        )

        explainer = shap.TreeExplainer(model)  # une seule fois après chargement
        shap_values = explainer.shap_values(features)
        explanation = dict(zip(serializer.fields, shap_values[0].tolist()))

        # Répondre à l’utilisateur
        return Response({
            "fraud": bool(prediction),
            "confidence": round(confidence, 2),
            "alerts": alerts,
            "explanation": explanation,
        })
    
    return Response(serializer.errors, status=400)
