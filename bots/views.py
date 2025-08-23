from rest_framework import viewsets, permissions
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import Bot, Scenario, Step
from .serializers import BotSerializer, ScenarioSerializer, StepSerializer
from .telegram_handler import telegram_handler

class BotViewSet(viewsets.ModelViewSet):
    serializer_class = BotSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Bot.objects.filter(owner=self.request.user)

class ScenarioViewSet(viewsets.ModelViewSet):
    serializer_class = ScenarioSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Scenario.objects.filter(bot__owner=self.request.user)

class StepViewSet(viewsets.ModelViewSet):
    serializer_class = StepSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Step.objects.filter(scenario__bot__owner=self.request.user)

@csrf_exempt
@require_POST
def telegram_webhook(request, bot_id):
    try:
        bot_model = Bot.objects.get(id=bot_id)
        dispatcher = telegram_handler.dispatchers.get(bot_model.id)
        
        if dispatcher:
            update = telegram.Update.de_json(json.loads(request.body), dispatcher.bot)
            dispatcher.process_update(update)
            return HttpResponse("OK")
        else:
            return HttpResponse("Bot not initialized", status=400)
            
    except Bot.DoesNotExist:
        return HttpResponse("Bot not found", status=404)
    except Exception as e:
        print(f"Webhook error: {e}")
        return HttpResponse("Error", status=500)