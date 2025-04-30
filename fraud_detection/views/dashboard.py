from django.shortcuts import render
from fraud_detection.models import PredictionLog
from collections import Counter
import datetime
import json

def dashboard_view(request):
    logs = PredictionLog.objects.all()

    # A. Fraudes par jour
    by_day = Counter(log.timestamp.date() for log in logs if log.predicted_fraud)
    days = sorted(by_day)
    counts = [by_day[day] for day in days]

    # B. Montants frauduleux
    fraud_amounts = [log.amount for log in logs if log.predicted_fraud]

    # C. Heures de fraude
    by_hour = Counter(log.time_encoded for log in logs if log.predicted_fraud)
    hours = list(range(24))
    hour_counts = [by_hour.get(h, 0) for h in hours]

    return render(request, "dashboard.html", {
        "days": json.dumps([str(d) for d in days]),
        "counts": json.dumps(counts),
        "amounts": json.dumps(fraud_amounts),
        "hour_counts": json.dumps(hour_counts),
        "hours": json.dumps(hours),
    })
