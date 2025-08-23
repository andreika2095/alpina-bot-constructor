from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BotViewSet, ScenarioViewSet, StepViewSet, telegram_webhook

router = DefaultRouter()
router.register(r'bots', BotViewSet)
router.register(r'scenarios', ScenarioViewSet)
router.register(r'steps', StepViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('telegram/webhook/<int:bot_id>/', telegram_webhook, name='telegram_webhook'),
]