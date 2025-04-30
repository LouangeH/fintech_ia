from django.db import models

class PredictionLog(models.Model):
    amount = models.FloatField()
    type_encoded = models.IntegerField()
    location_encoded = models.IntegerField()
    time_encoded = models.IntegerField()
    channel_encoded = models.IntegerField()
    balance_before = models.FloatField()
    balance_after =  models.FloatField()
    is_weekend = models.IntegerField()
    client_age_group = models.IntegerField()
    
    predicted_fraud = models.BooleanField()
    confidence = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {'FRAUDE' if self.predicted_fraud else 'OK'}"
