# bots/admin.py
from django.contrib import admin
from .models import Bot, Scenario, Step, UserSession

@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'created_at']
    list_filter = ['owner', 'created_at']

@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ['name', 'bot', 'created_at']
    list_filter = ['bot', 'created_at']

@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ['name', 'scenario', 'screen_type', 'created_at']
    list_filter = ['scenario', 'screen_type', 'created_at']

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'bot', 'is_active', 'created_at']
    list_filter = ['bot', 'is_active', 'created_at']