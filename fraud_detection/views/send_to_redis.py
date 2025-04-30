from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import redis

@csrf_exempt
def send_to_redis_view(request):
    success = False
    if request.method == "POST":
        try:
            data = {
                "user_id": request.POST.get("user_id"),
                "amount": request.POST.get("amount"),
                "type_encoded": request.POST.get("type_encoded"),
                "location_encoded": request.POST.get("location_encoded"),
                "time_encoded": request.POST.get("time_encoded"),
                "channel_encoded": request.POST.get("channel_encoded"),
                "balance_before": request.POST.get("balance_before"),
                "balance_after": request.POST.get("balance_after"),
                "is_weekend": request.POST.get("is_weekend"),
                "client_age_group": request.POST.get("client_age_group"),
            }
            r = redis.Redis()
            r.xadd("transactions", data)
            success = True
        except Exception as e:
            print("❌ Erreur Redis :", e)

    return render(request, "send_to_redis.html", {"success": success})
