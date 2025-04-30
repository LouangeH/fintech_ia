from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from fraud_detection.serializers import TransactionInputSerializer
from fraud_detection.models import PredictionLog
import joblib, os
import numpy as np

MODEL_PATH = os.path.join("ai_models", "fraud_model_xgb.pkl")
model = joblib.load(MODEL_PATH)

@csrf_exempt
def predict_form_view(request):
    result = None
    if request.method == "POST":
        form_data = {
            "amount": float(request.POST.get("amount", 0)),
            "type_encoded": int(request.POST.get("type_encoded", 0)),
            "location_encoded": int(request.POST.get("location_encoded", 0)),
            "time_encoded": int(request.POST.get("time_encoded", 0)),
            "channel_encoded": int(request.POST.get("channel_encoded", 0)),
            "balance_before": float(request.POST.get("balance_before", 0)),
            "balance_after": float(request.POST.get("balance_after", 0)),
            "is_weekend": int(request.POST.get("is_weekend", 0)),
            "client_age_group": int(request.POST.get("client_age_group", 0)),
        }

        serializer = TransactionInputSerializer(data=form_data)
        if serializer.is_valid():
            data = serializer.validated_data
            features = np.array([[data[f] for f in serializer.fields]])
            prediction = model.predict(features)[0]
            confidence = model.predict_proba(features)[0][1]
            result = {
                "fraud": bool(prediction),
                "confidence": round(confidence, 2)
            }

    return render(request, "predict_form.html", {"result": result})
