from rest_framework import serializers

class TransactionInputSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    type_encoded = serializers.IntegerField()
    location_encoded = serializers.IntegerField()
    time_encoded = serializers.IntegerField()
    channel_encoded = serializers.IntegerField()
    balance_before = serializers.FloatField()
    balance_after =  serializers.FloatField()
    is_weekend = serializers.IntegerField()
    client_age_group = serializers.IntegerField()