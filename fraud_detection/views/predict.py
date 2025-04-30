import random
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def predict_fraud(request):
    """
    simule une prediction de fraude a partir d'une transaction.
    """
    transaction_data = request.data
    # Exemple : Simulation basée sur le montant
    amount = float(transaction_data.get("amount",0))

    # Fausse logique si montant > 1000, plus de chance de fraude 
    fraud_probability = min(amount / 50000000, 1.0)
    is_fraud = fraud_probability > 0.7 or random.random() < 0.1 # seuil simple

    return Response({
        "fraud": is_fraud,
        "confidence": round(fraud_probability, 2)
    })