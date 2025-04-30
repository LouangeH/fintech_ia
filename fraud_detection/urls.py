# fraud_detection/urls.py
from django.urls import path
from .views import predict_fraud
from fraud_detection.views import predict_final, dashboard 

urlpatterns = [
    path('predict-fraud/', predict_fraud, name='predict_fraud'),
    path('fraude-predi/', predict_final.prediction_fraud, name='fraude_predi'),
    path("dashboard/", dashboard.dashboard_view, name="dashboard"),
]
