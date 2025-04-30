from django.contrib import admin
from .models import PredictionLog

@admin.register(PredictionLog)
class PredictionLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "amount", "type_encoded", "location_encoded", "time_encoded", "predicted_fraud", "confidence")
    list_filter = ("predicted_fraud", "timestamp")
    search_fields = ("amount", "location_encoded")
    ordering = ("-timestamp",)
