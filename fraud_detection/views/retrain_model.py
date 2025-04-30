from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render


@api_view(["POST"])
def retrain_model(request):
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from xgboost import XGBClassifier
    import joblib

    try:
        df = pd.read_csv("data/transactions_burundi_extended.csv")
        features = [
            "amount", "type_encoded", "location_encoded", "time_encoded",
            "channel_encoded", "balance_before", "balance_after",
            "is_weekend", "client_age_group"
        ]
        X = df[features]
        y = df["is_fraud"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y)
        model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
        model.fit(X_train, y_train)
        joblib.dump(model, "ai_models/fraud_model_xgb.pkl")
        return Response({"message": "✅ Modèle réentraîné avec succès."})
    except Exception as e:
        return Response({"error": str(e)}, status=500)
    

@ensure_csrf_cookie
def retrain_ui_view(request):
    return render(request, "retrain_model.html")

