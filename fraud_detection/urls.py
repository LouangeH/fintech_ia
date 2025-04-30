# fraud_detection/urls.py
from django.urls import path
from .views import predict_fraud
from fraud_detection.views import predict_final, dashboard , predict_form_view, retrain_model, retrain_ui_view

urlpatterns = [
    path('predict-fraud/', predict_fraud, name='predict_fraud'),
    path('fraude-predi/', predict_final.prediction_fraud, name='fraude_predi'),
    path("dashboard/", dashboard.dashboard_view, name="dashboard"),
    path("simulate/", predict_form_view, name="simulate_prediction"),
    path("retrain-model/", retrain_model, name="retrain_model"),
    path("retrain-ui/", retrain_ui_view, name="retrain_ui"),
]
